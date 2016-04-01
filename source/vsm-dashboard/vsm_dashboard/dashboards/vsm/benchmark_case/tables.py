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
from django.utils.translation import ugettext_lazy as _

from horizon import tables

STRING_SEPARATOR = "__"
LOG = logging.getLogger(__name__)


class AddBenchmarkCaseAction(tables.LinkAction):
    name = "add_benchmark_case"
    verbose_name = _("Create")
    classes = ('btn-primary',)
    url = "horizon:vsm:benchmark_case:index"

class DeleteBenchmarkCaseAction(tables.LinkAction):
    name = "delete_benchmark_case"
    verbose_name = _("Delete")
    classes = ('btn-primary',)
    url = "horizon:vsm:benchmark_case:index"

class BenchmarkCasesTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    name = tables.Column("name", verbose_name=_("Name"))
    ioengine = tables.Column("ioengine", verbose_name=_("IO Engine"))
    readwrite = tables.Column("readwrite", verbose_name=_("Read/Write"))
    running_hosts = tables.Column("running_hosts", verbose_name=_("Running Hosts"))
    status = tables.Column("status", verbose_name=_("Status"))

    class Meta:
        name = "benchmark_case_list"
        verbose_name = _("Benchmark Case List")
        multi_select = True
        table_actions = (AddBenchmarkCaseAction, DeleteBenchmarkCaseAction)


    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
