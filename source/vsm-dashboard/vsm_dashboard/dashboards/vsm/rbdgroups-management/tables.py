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

class AddRBDGroupAction(tables.LinkAction):
    name = "add_rbd_group"
    verbose_name = _("New")
    url = "/dashboard/vsm/rbdgroups-management/add_rbd_group_view/"
    classes = ('btn-primary',)

class RemoveRBDGroupsAction(tables.LinkAction):
    name = "remove_rbd_groups"
    verbose_name = _("Remove")
    classes = ('btn-primary',)
    url = "horizon:vsm:rbd_groups-management:index"



class RBDGroupsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name", verbose_name=_("Group Name"))
    comments = tables.Column("comments", verbose_name=_("Group Comments"))
    class Meta:
        name = "rbd_groups"
        verbose_name = _("RBD Group List")
        table_actions = (AddRBDGroupAction,RemoveRBDGroupsAction)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
