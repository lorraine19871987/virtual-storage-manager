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
        bm_cases = vsmapi.benchmark_case_get_all(self.request)
        return bm_cases['benchmark_cases']
