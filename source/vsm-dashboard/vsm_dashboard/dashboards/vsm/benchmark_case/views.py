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
import json

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from horizon import forms
from horizon import tables
from horizon import exceptions

from vsm_dashboard.api import vsm as vsmapi

from .tables import BenchmarkCasesTable

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):

    table_class = BenchmarkCasesTable
    template_name = 'vsm/benchmark_case/index.html'

    def get_data(self):
        case_list = []
        bm_cases = vsmapi.benchmark_case_get_all(self.request)
        for bm_case in bm_cases:
            case = {
                "id": bm_case.id,
                "name": bm_case.name,
                "ioengine": bm_case.ioengine,
                "readwrite": bm_case.readwrite,
                "running_hosts": bm_case.running_hosts,
                "status": bm_case.status
            }
            case_list.append(case)

        return case_list


def add_benchmark_case(request):
    pass

def delete_benchmark_case(request):
    data = json.loads(request.body)
    case_id_list = data["case_id_list"]

    for case_id in case_id_list:
        vsmapi.benchmark_case_delete(request, case_id)

    rs = json.dumps({"status":0})
    return HttpResponse(rs)