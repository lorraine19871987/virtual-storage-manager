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
    _collection_name = "snapshots"
    def _detail(self, request, snapshot):
        LOG.info("snapshot api detail view %s " % snapshot)
        #LOG.info("snapshot api detail view 2222 %s " % type(snapshot['updated_at']))
        snapshot = {
                "id": snapshot.id,
                "name":snapshot.name,
                "pool": snapshot.pool,
                "image": snapshot.image,
                "snap_id":snapshot.snap_id,
                "created_at": snapshot.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status":snapshot.status,
                "size":snapshot.size,
        }

        return snapshot

    def detail(self, request, snapshots):
        return self._list_view(self._detail, request, snapshots)



    def _list_view(self, func, request, snapshots):
        """Provide a view for a list of snapshots."""
        snapshot_list = [func(request, snapshot) for snapshot in snapshots]
        snapshots_dict = dict(snapshots=snapshot_list)
        return snapshots_dict