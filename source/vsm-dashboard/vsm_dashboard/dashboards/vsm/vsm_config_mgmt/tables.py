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


from django.utils.translation import ugettext_lazy as _

from horizon import tables


class UpdateVSMConfig(tables.LinkAction):
    name = "update"
    verbose_name = _("Update")
    url = "horizon:vsm:vsm_config_mgmt:update"
    classes = ("ajax-modal", "btn-primary")

class ListVSMConfigTable(tables.DataTable):

    id = tables.Column("id", verbose_name=_("ID"), classes=("vsm_config_list",),hidden=True)
    name = tables.Column("name", verbose_name=_("Name"))
    section = tables.Column("section", verbose_name=_("Section"))
    default_value = tables.Column("default_value", verbose_name=_("Default Value"))
    value = tables.Column("value", verbose_name=_("Current Value"))
    description = tables.Column("description", verbose_name=_("Description"))

    class Meta:
        name = "vsm_config_list"
        verbose_name = _("VSM Config List")
        row_actions = (UpdateVSMConfig, )
        multi_select = False

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]

    def get_object_display(self, datum):
        if hasattr(datum, "name"):
            return datum.name
        else:
            return datum["name"]
