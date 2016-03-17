# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Corporation, All Rights Reserved.
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

import logging
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import exceptions
from horizon import messages
from vsm_dashboard.api import vsm as vsmapi

LOG = logging.getLogger(__name__)

class AddSnapshotAction(tables.LinkAction):
    name = "add_snapshot"
    verbose_name = _("New")
    url = "/dashboard/vsm/snapshots-management/add_snapshot_view/"
    classes = ('btn-primary',)

class RemoveSnapshotsAction(tables.LinkAction):
    name = "remove_snapshots"
    verbose_name = _("Remove")
    classes = ('btn-primary',)
    url = "horizon:vsm:snapshots-management:index"



class SnapshotsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    snapshot_name = tables.Column("snapshot_name", verbose_name=_("Snapshot Name"))
    pool = tables.Column("snap_id", verbose_name=_("Snap ID"))
    snap_id = tables.Column("pool", verbose_name=_("Pool"))
    image_name = tables.Column("image_name", verbose_name=_("Image Name"))
    created_at = tables.Column("created_at", verbose_name=_("Created at"))
    class Meta:
        name = "snapshots"
        verbose_name = _("Snapshot List")
        table_actions = (AddSnapshotAction,RemoveSnapshotsAction,)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
