# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the"License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""The benchmark_cases api."""


import uuid
from webob import exc

from vsm.agent import rpcapi
from vsm.api.openstack import wsgi
from vsm.api.views import benchmark_cases as bc_views
from vsm import conductor
from vsm import db
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import scheduler

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS


class BenchmarkCaseController(wsgi.Controller):
    """The BenchmarkCase API controller for the VSM API."""

    _view_builder_class = bc_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        self.agent_rpcapi = rpcapi.AgentAPI()
        self.ext_mgr = ext_mgr
        super(BenchmarkCaseController, self).__init__()


    def show(self, req, id):
        """Return data about the given benchmark case."""

        context = req.environ['vsm.context']

        try:
            benchmark_case = self.conductor_api.benchmark_case_get(context, id)
            return self._view_builder.show(req, benchmark_case)
        except exception.NotFound:
            raise exc.HTTPNotFound()


    def index(self, req):
        """Return the list of benchmark cases."""

        return self._items(req, entity_maker=self._view_builder.index)

    def _items(self, req, entity_maker):
        """Returns a list of benchmark cases."""

        filters = req.GET.copy()
        limit = filters.pop('limit', None)
        marker = filters.pop('marker', None)
        sort_key = filters.pop('sort_key', None)
        sort_dir = filters.pop('sort_dir', None)

        context = req.environ['vsm.context']

        search_opts = {}
        name = filters.pop('name', None)
        if name:
            search_opts["name"] = name

        LOG.info("Search_opts is " + str(search_opts))
        cases = self.conductor_api.benchmark_case_get_all(context, marker=marker,
                                                          limit=limit,
                                                          sort_key=sort_key,
                                                          sort_dir=sort_dir,
                                                          filters=search_opts)
        return entity_maker(req, cases)


    def create(self, req, body):
        """
        Create a benchmark case.
        :param req:
        :param body:
            As example:
            {
              "benchmark_case": {
                "name": "case1",
                "readwrite": "randrw",
                "blocksize": "4k",
                "iodepth": 64,
                "runtime": 60,
                "ioengine": "rbd",
                "clientname": "admin",
                "additional_options": ""
              }
            }
        :return:
        """

        context = req.environ['vsm.context']

        benchmark_case = body['benchmark_case']
        self.validate_required_parameters(
            benchmark_case, ['name', 'readwrite', 'blocksize', 'iodepth',
                             'runtime', 'ioengine', 'clientname'])
        case_name = benchmark_case.get('name')
        kwargs = {}
        # readwrite can be read, write, rw, randread, randwrite or randrw
        readwrite = benchmark_case.get('readwrite')
        kwargs['readwrite'] = readwrite
        kwargs['blocksize'] = benchmark_case.get('blocksize')
        kwargs['iodepth'] = benchmark_case.get('iodepth')
        # ioengine now only support rbd
        ioengine = benchmark_case.get('ioengine')
        if ioengine != 'rbd':
            LOG.error("Only support rbd ioengine now!")
            raise exception.InvalidParameterValue(message="Only support rbd ioengine now!")
        kwargs['ioengine'] = ioengine
        kwargs['clientname'] = benchmark_case.get('clientname')

        # additional options format: k:v;;k:v
        kwargs['additional_options'] = benchmark_case.get('additional_options', None)

        LOG.info("===============create benchmark case, parameters are %s" % str(kwargs))
        self.conductor_api.benchmark_case_create(context, case_name, **kwargs)
        LOG.info("===============create benchmark case successfully")


    def delete(self, req, id):
        """Delete a config by a given id."""

        context = req.environ['vsm.context']

        try:
            case = self.conductor_api.benchmark_case_get(context, id)
        except exception.NotFound:
            raise exc.HTTPNotFound()

        status = case.get('status')
        if status == "running":
            LOG.error("The case is still running, please wait for a moment")
            raise exc.HTTPBadRequest()

        try:
            self.conductor_api.benchmark_case_delete(context, id)
        except:
            raise exc.HTTPError()

        pass


    def update(self, req, id, body):
        """Update a config."""

        pass


    def run_case(self, req, id, body):
        """

        :param req:
        :param id:
        :param body:
            As example:
            {
              "benchmark_info": [
                {
                  "host": "vsm-node1",
                  "pool_rbd": [
                    {"pool": "tp001", "rbds": "volume01,volume02,volume03", "rbd_num": 3, "rbd_size": ""},
                    {"pool": "tp002", "rbds": "volume04", "rbd_num": 1, "rbd_size": ""}
                  ]
                },
                {
                  "host": "vsm-node2",
                  "pool_rbd": [
                    {"pool": "tp003", "rbds": "", "rbd_num": 1, "rbd_size": "1024"}
                  ]
                }
              ]
            }
        :return:
        """

        context = req.environ['vsm.context']

        try:
            case = self.conductor_api.benchmark_case_get(context, id)
            LOG.info("===============get benchmark case %s"
                     % str(self._view_builder.show(req, case, brief=True)))
        except exception.NotFound:
            LOG.error("Not found the benchmark case")
            raise exc.HTTPNotFound()
        if case.get('status') == "running":
            LOG.error("The case is still running, please wait for a moment")
            raise exc.HTTPBadRequest()

        benchmark_info_list = body['benchmark_info']
        LOG.info("===============benchmark_info_list: %s" % str(benchmark_info_list))
        if len(benchmark_info_list) < 1:
            LOG.error("Need one benchmark info at least")
            raise exception.NotFound(message="Need one benchmark info at least")

        new_volumes_list_total = []
        for benchmark_info in benchmark_info_list:
            pool_rbd_list = benchmark_info['pool_rbd']
            for pool_rbd in pool_rbd_list:
                new_volumes_list = []
                rbds = pool_rbd['rbds']
                # create new rbds if not rbds
                if not rbds:
                    poolname = pool_rbd['pool']
                    pool = db.pool_get_by_name(context, poolname, "1")
                    rbd_num = int(pool_rbd['rbd_num'] or 1)
                    # rbd default size 1024MB
                    rbd_size = pool_rbd['rbd_size'] or 1024
                    while rbd_num > 0:
                        create_rbds = {}
                        create_rbds['rbds'] = []
                        volume_name = "volume-" + str(uuid.uuid4())
                        create_rbds['rbds'].append({
                            "pool": pool.get("pool_id"),
                            "image": volume_name,
                            "size": rbd_size,
                            "format": 2})
                        LOG.info("==================create_rbds: %s" % str(create_rbds))
                        self.scheduler_api.add_rbd(context, create_rbds)
                        new_volumes_list.append(volume_name)
                        new_volumes_list_total.append(volume_name)
                        rbd_num = rbd_num - 1
                    pool_rbd['rbds'] = ",".join(new_volumes_list)
        LOG.info("===============new benchmark_info_list: %s" % str(benchmark_info_list))
        try:
            self.scheduler_api.benchmark_case_run(context, benchmark_info_list, case)
        except:
            LOG.error("Failed to run the benchmark case %s" % str(case.get('name')))

        # TODO Delete the rbd created by the benchmark or not
        if new_volumes_list_total:
            try:
                pass
            except:
                pass


    def validate_required_parameters(self, case, required_parameters):
        for paramter in required_parameters:
            parameter_value = case.get(paramter, '')
            if not parameter_value:
                LOG.error("Required parameter %s is missing" % paramter)
                raise exception.InvalidParameterValue(message="Required parameter %s is "
                                                              "missing" % paramter)

    def terminate(self, req, id):
        """Terminate a running benchmark case."""

        context = req.environ['vsm.context']

        try:
            benchmark_case = self.conductor_api.benchmark_case_get(context, id)
        except exception.NotFound:
            raise exc.HTTPNotFound()

        if benchmark_case.get('status') != "running":
            LOG.error("Only running case can be terminated")
            raise exc.HTTPBadRequest()
        running_hosts = benchmark_case.get('running_hosts')
        if not running_hosts:
            LOG.error("Miss running hosts, please terminate fio manually this time")
            raise exc.HTTPBadRequest()
        hosts_list = running_hosts.split(",")
        for host in hosts_list:
            self.agent_rpcapi.benchmark_case_terminate(context, host)

        # update the status from running to terminated, set running_host to blank
        values = {}
        values['status'] = 'terminated'
        values['running_hosts'] = ''
        self.conductor_api.benchmark_case_update(context, id, values)

def create_resource(ext_mgr):
    return wsgi.Resource(BenchmarkCaseController(ext_mgr))
