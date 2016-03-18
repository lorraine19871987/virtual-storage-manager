# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from vsm.api import common
import logging
import time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = "rbd_groups"
    def _detail(self, request, rbd_group):
        LOG.info("rbd_groups api detail view %s " % rbd_group)
        #LOG.info("snapshot api detail view 2222 %s " % type(snapshot['updated_at']))
        rbd_group = {
                "id": rbd_group.id,
                "name":rbd_group.name,
                "comments": rbd_group.comments,
        }

        return rbd_group

    def detail(self, request, rbd_groups):
        LOG.info('rbd detail view-----%s'%rbd_groups)
        return self._list_view(self._detail, request, rbd_groups)



    def _list_view(self, func, request, rbd_groups):
        """Provide a view for a list of snapshots."""
        rbd_group_list = [func(request, group) for group in rbd_groups]
        rbd_group_dict = dict(rbd_groups=rbd_group_list)
        return rbd_group_dict