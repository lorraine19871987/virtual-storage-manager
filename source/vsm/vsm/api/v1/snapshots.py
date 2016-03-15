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
def make_snapshot(elem, detailed=False):
    elem.set('id')
    elem.set('snapshot_name')
    elem.set('pool')
    elem.set('image_name')
    elem.set('created_at')


    if detailed:
        pass

snapshot_nsmap = {None: xmlutil.XMLNS_V11, 'atom': xmlutil.XMLNS_ATOM}

class OSDTemplate(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('osd', selector='osd')
        make_snapshot(root, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=snapshot_nsmap)

class SnapShotsTemplate(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('snapshots')
        elem = xmlutil.SubTemplateElement(root, 'snapshot', selector='snapshot')
        make_snapshot(elem, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=snapshot_nsmap)


class SnapShotController(wsgi.Controller):
    """The Snapshot API controller for the Snapshot API."""
    _view_builder_class = snapshot_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr

        # at this point, we will add the map as an data member
        # about storage_group and pool_size
        #self.group_map = scheduler_api.

        super(SnapShotController, self).__init__()

    def detail(self, req):
        """Returns the list of snapshots."""
        LOG.info("Get a list of snapshots")
        context = req.environ['vsm.context']
        snapshots = db.snapshot_get_all(context)
        return self._view_builder.detail(req, snapshots)

    def snapshot_create(self, req, body=None):
        LOG.info('CEPH_LOG snapshot_create body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.rbd_snapshot_create(context,body)

    def snapshot_remove(self, req, body=None):
        LOG.info('CEPH_LOG snapshot_remove body %s ' % body)
        context = req.environ['vsm.context']
        return self.scheduler_api.rbd_snapshot_remove(context,body)

def create_resource(ext_mgr):
    return wsgi.Resource(SnapShotController(ext_mgr))

