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


from vsm.api.openstack import wsgi
from vsm import flags


from vsm import scheduler
from vsm import db
from vsm.api.views import snapshots as snapshot_views
from vsm.api import xmlutil
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS

def make_rbd_group(elem, detailed=False):
    elem.set('id')
    elem.set('name')
    elem.set('comments')
    if detailed:
        pass
rbd_group_nsmap = {None: xmlutil.XMLNS_V11, 'atom': xmlutil.XMLNS_ATOM}



class RBDGroupsTemplate(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('rbd_groups')
        elem = xmlutil.SubTemplateElement(root, 'rbd_group', selector='rbd_group')
        make_rbd_group(elem, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=rbd_group_nsmap)


class RBDGroupController(wsgi.Controller):
    """The Snapshot API controller for the Snapshot API."""
    _view_builder_class = snapshot_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr
        super(RBDGroupController, self).__init__()

    def detail(self, req):
        """Returns the list of snapshots."""
        LOG.info("Get a list of rbdgroups")
        context = req.environ['vsm.context']
        snapshots = db.rbd_groups_get_all(context)
        return self._view_builder.detail(req, snapshots)

    def rbd_group_create(self, req, body=None):
        LOG.info('CEPH_LOG rbd_group_create body %s ' % body)
        context = req.environ['vsm.context']
        for group in body.get('rbd_groups'):
            db.rbd_group_create(context,group)
        return {}

    def rbd_group_update(self, req, body=None):
        LOG.info('CEPH_LOG rbd_group_update body %s ' % body)
        context = req.environ['vsm.context']
        for group in body.get('rbd_groups'):
            db.rbd_group_update(context,group['id'],group)
        return {}

    def rbd_group_remove(self, req, body=None):
        LOG.info('CEPH_LOG rbd_group_remove body %s ' % body)
        context = req.environ['vsm.context']
        for group_id in body.get('rbd_groups'):
            db.rbd_group_remove(context,group_id)
        return {}

def create_resource(ext_mgr):
    return wsgi.Resource(RBDGroupController(ext_mgr))

