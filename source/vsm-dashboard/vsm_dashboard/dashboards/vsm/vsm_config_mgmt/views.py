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
from django.views.generic import TemplateView

from vsm_dashboard.api import vsm as vsmapi

LOG = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'vsm/vsm_config_mgmt/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        print "=============name: %s" % name
        search_opts = {'category': "VSM", 'name': name}
        vsm_configs = vsmapi.config_get_all(self.request, search_opts=search_opts)
        context['settings'] = vsm_configs
        return context

def SettingsAction(request, action):
    data = json.loads(request.body)
    print "=================data: %s" % data
    try:
        config_id = data['config_id']
        config_value = data['config_value']
        config_section = data['config_section']
        config_description = data['config_description']
        vsmapi.config_update(request, config_id, section=config_section,
                             value=config_value, description=config_description)
        resp = dict(message="Succeed to update VSM Config", status="success", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
    except:
        resp = dict(message="Fail to update VSM Config", status="error", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
