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

import webob
from webob import exc
from vsm.api.openstack import wsgi
from vsm.api import xmlutil
from vsm import flags
from vsm.openstack.common import log as logging
from vsm.api.views import rbd_pools as rbd_pool_views
from vsm import conductor
from vsm import scheduler
from vsm import exception
from vsm import db
import datetime,time

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS

def make_rbd_pool(elem, detailed=False):
    elem.set('id')
    elem.set('name')
    elem.set('address')
    elem.set('health')
    elem.set('detail')
    elem.set('skew')
    elem.set('latency')
    elem.set('kb_total')
    elem.set('kb_used')
    elem.set('kb_avail')
    elem.set('percent_avail')

    if detailed:
        pass

rbd_pool_nsmap = {None: xmlutil.XMLNS_V11, 'atom': xmlutil.XMLNS_ATOM}

class RBDPoolTemplate(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('rbd_pool', selector='rbd_pool')
        make_rbd_pool(root, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=rbd_pool_nsmap)

class RBDPoolsTemplate(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('rbd_pools')
        elem = xmlutil.SubTemplateElement(root, 'rbd_pool', selector='rbd_poolss')
        make_rbd_pool(elem, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=rbd_pool_nsmap)

class Controller(wsgi.Controller):
    """The rbd_pools API controller for the OpenStack API."""
    _view_builder_class = rbd_pool_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr
        super(Controller, self).__init__()

    #def _get_zone_search_options(self):
    #    """Return zone search options allowed by non-admin."""
    #    return ('id', 'name', 'public_ip')

    def _get_rbd_pool(self, context, req, id):
        """Utility function for looking up an instance by id."""
        try:
            rbd_pool = self.conductor_api.rbd_pool_get(context, id)
        except exception.NotFound:
            msg = _("rbd_pool could not be found")
            raise exc.HTTPNotFound(explanation=msg)
        return rbd_pool

    @wsgi.serializers(xml=RBDPoolsTemplate)
    def show(self, req, id):
        """Return data about the given rbd_pool."""
        context = req.environ['vsm.context']

        try:
            rbd_pool = self._get_rbd_pool(context, req, id)
        except exception.NotFound:
            raise exc.HTTPNotFound()

        return {'rbd_pool': rbd_pool}

    @wsgi.serializers(xml=RBDPoolsTemplate)
    def index(self, req):
        """Return a list of rbd pools."""

        context = req.environ['vsm.context']
        limit = req.GET.get('limit', None)
        marker = req.GET.get('marker', None)
        sort_keys = req.GET.get('sort_keys', None)
        sort_dir = req.GET.get('sort_dir', None)

        rbd_pools = self.conductor_api.rbd_get_all(context,
                                                   limit=limit,
                                                   marker=marker,
                                                   sort_keys=sort_keys,
                                                   sort_dir=sort_dir)
        LOG.info('vsm/api/v1/rbd_pool.py rbd_pools:%s' % rbd_pools)

        return self._view_builder.index(req, rbd_pools)

    @wsgi.serializers(xml=RBDPoolsTemplate)
    def detail(self, req):

        """Get rbd_pool list."""
        #search_opts = {}
        #search_opts.update(req.GET)
        context = req.environ['vsm.context']
        #remove_invalid_options(context,
        #                        search_opts,
        #                        self._get_zone_search_options)
        #zones = self.conductor_api.get_zone_list(context)
        limit = req.GET.get('limit', None)
        marker = req.GET.get('marker', None)
        sort_keys = req.GET.get('sort_keys', None)
        sort_dir = req.GET.get('sort_dir', None)

        rbd_pools = self.conductor_api.rbd_get_all(context, limit, marker,
						   sort_keys, sort_dir)
        LOG.info('vsm/api/v1/rbd_pools.py detailed rbd_pools:%s' % rbd_pools)
        rbd_images = []
        for rbd_image in rbd_pools:
            if rbd_image[0]['parent_snapshot']:
                rbd_image[0]['parent_snapshot_detail'] = '%s/%s@%s'%(rbd_image[1]['pool'],\
                                                                rbd_image[1]['image'],rbd_image[1]['name'])
            rbd_image[0]['group_name'] = rbd_image[0]['group']['name']
            auto_snapshot_interval = rbd_image[0]['auto_snapshot_interval']
            auto_snapshot_start = rbd_image[0]['auto_snapshot_start']
            if auto_snapshot_start and auto_snapshot_interval:
                auto_snapshot_start_datetime = datetime.datetime.strptime(auto_snapshot_start.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                auto_snapshot_start_time = time.mktime(time.strptime(auto_snapshot_start.split('.')[0], "%Y-%m-%dT%H:%M:%S"))
                now_time = time.time()
                snap_times = int(now_time-auto_snapshot_start_time)/3600%auto_snapshot_interval
                pre_snap_time = auto_snapshot_start_datetime + datetime.timedelta(hours=auto_snapshot_interval * snap_times)
                next_snap_time = pre_snap_time + datetime.timedelta(hours=auto_snapshot_interval)
                rbd_image[0]['pre_snap_time'] = pre_snap_time.strftime("%Y-%m-%d %H")
                rbd_image[0]['next_snap_time'] = next_snap_time.strftime("%Y-%m-%d %H")
            rbd_images.append(rbd_image[0])
        return self._view_builder.detail(req, rbd_images)

    def summary(self, req, body=None):
        LOG.info('CEPH_LOG rbd_pool-summary body %s ' % body)
        context = req.environ['vsm.context']
        return {'rbd-summary':{'epoch': 123,
                               'num_rbd_pools': 12,
                               'num_up_rbd_pools': 8,
                               'num_in_rbd_pools': 8,
                               'nearfull': False,
                               'full': False,
                               }}

    def snapshot_get_by_rbd_id(self, req, body=None):
        LOG.info('CEPH_LOG snapshot_get_by_rbd_id body %s ' % body)
        context = req.environ['vsm.context']
        rbd_id = req.GET.get('rbd_id')
        rbd = db.rbd_get(context,rbd_id)
        snaps = db.snapshot_get_by_pool_image(context,rbd.pool,rbd.image)
        LOG.info('CEPH_LOG snapshot_get_by_rbd_id snaps %s ' % snaps)
        return {'snapshots':snaps}

    def add_rbd(self, req, body=None):
        LOG.info('CEPH_LOG add_rbd body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.add_rbd(context,body)

    def remove_rbd(self, req, body=None):
        LOG.info('CEPH_LOG remove_rbd body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.remove_rbd(context,body)

    def flatten_rbd(self, req, body=None):
        LOG.info('CEPH_LOG flatten_rbd body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.flatten_rbd(context,body)

    def clone_rbd(self, req, body=None):
        LOG.info('CEPH_LOG clone_rbd body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.clone_rbd(context,body)

    def rbd_snapshot_create(self, req, body=None):
        LOG.info('CEPH_LOG rbd_snapshot_create body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.rbd_snapshot_create(context,body)

    def rbd_snapshot_remove(self, req, body=None):
        LOG.info('CEPH_LOG rbd_snapshot_remove body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.rbd_snapshot_remove(context,body)

    def rbd_snapshot_rollback(self, req, body=None):
        LOG.info('CEPH_LOG rbd_snapshot_rollback body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.rbd_snapshot_rollback(context,body)

def create_resource(ext_mgr):
    return wsgi.Resource(Controller(ext_mgr))

#def remove_invalid_options(context, search_options, allowed_search_options):
#    """Remove search options that are not valid for non-admin API/context."""
#    if context.is_admin:
#        # Allow all options
#        return
#    # Otherwise, strip out all unknown options
#    unknown_options = [opt for opt in search_options
#                       if opt not in allowed_search_options]
#    bad_options = ", ".join(unknown_options)
#    log_msg = _("Removing options '%(bad_options)s' from query") % locals()
#    LOG.debug(log_msg)
#    for opt in unknown_options:
#        del search_options[opt]
