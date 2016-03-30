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
import webob
from webob import exc

from vsm.api.openstack import wsgi
from vsm.api.views import benchmark_cases as bc_views
from vsm import conductor
from vsm import db
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm.openstack.common import timeutils
from vsm import scheduler

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS


class BenchmarkCaseController(wsgi.Controller):
    """The BenchmarkCase API controller for the VSM API."""

    _view_builder_class = bc_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr
        super(BenchmarkCaseController, self).__init__()


    def show(self, req, id):
        """Return data about the given config."""

        pass


    def index(self, req):
        """Returns the list of configs."""

        pass


    def create(self, req, body):
        """Create a benchmark case."""

        context = req.environ['vsm.context']

        benchmark_case = body['benchmark_case']
        self.validate_required_parameters(
            benchmark_case, ['name', 'direct', 'time_based', 'readwrite',
                             'blocksize', 'iodepth', 'ramp_time', 'runtime',
                             'ioengine', 'clientadmin', 'iodepth_batch_submit',
                             'iodepth_batch_complete'])
        case_name = benchmark_case.get('name')
        kwargs = {}
        kwargs['direct'] = benchmark_case.get('direct')
        kwargs['time_based'] = benchmark_case.get('time_based')
        # readwrite can be read, write, rw, randread, randwrite or randrw
        readwrite = benchmark_case.get('readwrite')
        kwargs['readwrite'] = readwrite
        kwargs['blocksize'] = benchmark_case.get('blocksize')
        kwargs['iodepth'] = benchmark_case.get('iodepth')
        kwargs['ramp_time'] = benchmark_case.get('ramp_time')
        kwargs['runtime'] = benchmark_case.get('runtime')
        # ioengine now only support rbd
        ioengine = benchmark_case.get('ioengine')
        if ioengine != 'rbd':
            LOG.error("Only support rbd ioengine now!")
            raise exception.InvalidParameterValue(message="Only support rbd ioengine now!")
        kwargs['ioengine'] = ioengine
        kwargs['clientadmin'] = benchmark_case.get('clientadmin')

        # readwrite is randread, randwrite or randrw
        if readwrite in ['randread', 'randwrite', 'randrw']:
            kwargs['iodepth_batch_submit'] = benchmark_case.get('iodepth_batch_submit')
            kwargs['iodepth_batch_complete'] = benchmark_case.get('iodepth_batch_complete')
            kwargs['norandommap'] = benchmark_case.get('norandommap', None)
            kwargs['randrepeat'] = benchmark_case.get('randrepeat', None)
            kwargs['rate_iops'] = benchmark_case.get('rate_iops', None)
            kwargs['random_distribution'] = benchmark_case.get('random_distribution', None)

        # readwrite is read, write or rw
        if readwrite in ['read', 'write', 'rw']:
            kwargs['iodepth_batch_submit'] = benchmark_case.get('iodepth_batch_submit')
            kwargs['iodepth_batch_complete'] = benchmark_case.get('iodepth_batch_complete')
            kwargs['rate'] = benchmark_case.get('rate', None)

        # readwrite is randrw or rw
        if readwrite in ['randrw', 'rw']:
            kwargs['rwmixread'] = benchmark_case.get('rwmixread', None)

        # additional options format: k:v;;k:v
        kwargs['additional_options'] = benchmark_case.get('additional_options', None)

        LOG.info("===============create benchmark case, parameters are %s" % str(kwargs))
        self.conductor_api.benchmark_case_create(context, case_name, **kwargs)
        LOG.info("===============create benchmark case successfully")


    def delete(self, req, id):
        """Delete a config by a given id."""

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
        except:
            LOG.error("Not found the benchmark case")
            raise exc.HTTPNotFound()

        benchmark_info_list = body['benchmark_info']
        LOG.info("===============benchmark_info_list: %s" % str(benchmark_info_list))
        if len(benchmark_info_list) < 1:
            LOG.error("Need one benchmark info at least")
            raise exception.NotFound(message="Need one benchmark info at least")

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
                            "format": 2
                        })
                        LOG.info("==================create_rbds: %s" % str(create_rbds))
                        self.scheduler_api.add_rbd(context, create_rbds)
                        new_volumes_list.append(volume_name)
                        rbd_num = rbd_num - 1
                    pool_rbd['rbds'] = ",".join(new_volumes_list)
        LOG.info("===============new benchmark_info_list: %s" % str(benchmark_info_list))
        try:
            self.scheduler_api.benchmark_case_run(context, benchmark_info_list, case)
        except:
            pass


    def validate_required_parameters(self, case, required_parameters):
        for paramter in required_parameters:
            parameter_value = case.get(paramter, '')
            if not parameter_value:
                LOG.error("Required parameter %s is missing" % paramter)
                raise exception.InvalidParameterValue(message="Required parameter %s is "
                                                              "missing" % paramter)

def create_resource(ext_mgr):
    return wsgi.Resource(BenchmarkCaseController(ext_mgr))
