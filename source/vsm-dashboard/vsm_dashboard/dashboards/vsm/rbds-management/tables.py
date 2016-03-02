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

STRING_SEPARATOR = "__"
LOG = logging.getLogger(__name__)

class FlattenRBDsAction(tables.LinkAction):
    name = "flatten_rbds"
    verbose_name = _("Flatten")
    classes = ('btn-primary',)
    url = "horizon:vsm:rbds-management:index"

class RemoveRBDsAction(tables.LinkAction):
    name = "remove_rbds"
    verbose_name = _("Remove")
    classes = ('btn-primary',)
    url = "horizon:vsm:rbds-management:index"

class CreateRBDAction(tables.LinkAction):
    name = "create_rbd"
    verbose_name = _("New")
    url = "/dashboard/vsm/rbds-management/create_new_rbd/"
    classes = ('btn-primary',)



class RBDsTable(tables.DataTable):
    STATUS_CHOICES = (
        ("active", True),
        ("available", True),
        ("Active", True),
    )

    id = tables.Column("id", verbose_name=_("ID"))
    pool = tables.Column("pool", verbose_name=_("Pool"))
    image_name = tables.Column("image_name", verbose_name=_("Image Name"))
    size = tables.Column("size", verbose_name=_("Size(MB)"))
    objects = tables.Column("objects", verbose_name=_("Objects"))
    order = tables.Column("order", verbose_name=_("Order"))
    format = tables.Column("format", verbose_name=_("Format"))
    updated_at = tables.Column("updated_at", verbose_name=_("Updated at"), classes=("span2",))
    parent_snapshot = tables.Column("parent_snapshot", verbose_name=_("Parent Snapshot"))
    class Meta:
        name = "rbd_list"
        verbose_name = _("RBD List")
        multi_select = True
        table_actions = (RemoveRBDsAction,CreateRBDAction,)


    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
