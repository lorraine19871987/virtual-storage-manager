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


# class UpdateRow(tables.Row):
#     ajax = False
#
#     def get_data(self, request, osd_id):
#         osd = vsmapi.osd_get(request, osd_id)
#         return osd
#
# class RestartOsdsAction(tables.LinkAction):
#     name = "restart_osds"
#     verbose_name = _("Restart")
#     classes = ('btn-primary',)
#     url = "horizon:vsm:devices-management:index"
#
#
# class RemoveOsdsAction(tables.LinkAction):
#     name = "remove_osds"
#     verbose_name = _("Remove")
#     classes = ('btn-primary',)
#     url = "horizon:vsm:devices-management:index"
#
#
# class RestoreOsdsAction(tables.LinkAction):
#     name = "restore_osds"
#     verbose_name = _("Restore")
#     classes = ('btn-primary',)
#     url = "horizon:vsm:devices-management:index"
#
#
# class AddOsdsAction(tables.BatchAction):
#     name = "Add_osds"
#     action_present = _("Add")
#     action_past = _("Scheduled add of")
#     data_type_singular = _("Osd")
#     data_type_plural = _("Osds")
#     classes = ('btn-primary',)
#     redirect_url = "horizon:vsm:devices-management:index"
#
#     def allowed(self, request, osd=None):
#         if osd is not None:
#             if osd['vsm_status'] not in UNINIT_STATES:
#                 msg = _('Only osd with VSM status "%s" will be added'%UNINIT_STATES)
#                 messages.error(request, msg)
#                 return False
#         return True
#
#     def action(self, request, obj_id):
#         obj = self.table.get_object_by_id(obj_id)
#         name = self.table.get_object_display(obj)
#         try:
#             vsmapi.add_osd_from_node_in_cluster(request, obj_id)
#         except Exception:
#             msg = _('Error adding %s.' % name)
#             LOG.info(msg)
#             redirect = reverse(self.redirect_url)
#             exceptions.handle(request, msg, redirect=redirect)
#
# STATUS_DISPLAY_CHOICES = (
#     ("removing", "Removing"),
#     ("restarting", "Restarting"),
#     ("restoring", "Restoring"),
# )
#
# class AddOSDAction(tables.LinkAction):
#     name = "add_osd"
#     verbose_name = _("New")
#     url = "/dashboard/vsm/devices-management/add_new_osd/"
#     classes = ('btn-primary',)

class SnapshotsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    #id = Column(Integer, primary_key=True, nullable=False)
    snapshot_name = tables.Column("snapshot_name", verbose_name=_("Snapshot Name"))
    pool = tables.Column("pool", verbose_name=_("Pool"))
    image_name = tables.Column("image_name", verbose_name=_("Image Name"))
    created_at = tables.Column("created_at", verbose_name=_("Created at"))
    class Meta:
        name = "snapshots"
        verbose_name = _("Snapshot List")
        table_actions = ()
        #row_class = UpdateRow

    # def get_object_id(self, obj):
    #     return obj["id"]
    #
    # def get_object_by_id(self, obj_id):
    #     for obj in self.data:
    #         if self.get_object_id(obj) == int(obj_id):
    #             return obj
    #     raise ValueError('No match found for the id "%s".' % obj_id)
    #
    # def get_object_display(self, obj):
    #     return obj["osd"]
    #
