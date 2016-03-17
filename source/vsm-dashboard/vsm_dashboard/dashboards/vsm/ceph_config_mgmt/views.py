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
from horizon import exceptions

from vsm_dashboard.api import vsm as vsmapi

from .forms import CreateCephConfigForm
from .forms import UpdateCephConfigForm

LOG = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'vsm/ceph_config_mgmt/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        search_opts = {'category': "CEPH", 'name': name}
        ceph_config = vsmapi.config_get_all(self.request, search_opts=search_opts)
        if ceph_config:
            _ceph_config = []
            for config in ceph_config:
                if config.section != "":
                    _ceph_config.append({
                        "name": config.name,
                        "value": config.value,
                        "id": config.id,
                        "alterable": config.alterable,
                        "section": config.section,
                        "description": config.description,
                        "default_value": config.default_value,
                        "category": config.category
                    })
            ceph_config = _ceph_config
            sort_on = "section"
            decorated = [(dict_[sort_on], dict_) for dict_ in ceph_config]
            decorated.sort()
            ceph_config = [dict_ for (key, dict_) in decorated]

            section = ""
            new_ceph_config = []
            new_dict = {}
            for config in ceph_config:
                if config["section"].split('.')[0] != section:
                    new_ceph_config.append(new_dict)
                    new_dict = {}
                    new_dict['section'] = config["section"].split('.')[0]
                    new_dict['items'] = []
                    section = config["section"].split('.')[0]
                new_dict['items'].append(config)
            new_ceph_config.append(new_dict)
            new_ceph_config.pop(0)
        else:
            ceph_global_config = {}
            ceph_global_config['section'] = 'global'
            ceph_global_config['items'] = []
            ceph_mon_config = {}
            ceph_mon_config['section'] = 'mon'
            ceph_mon_config['items'] = []
            ceph_osd_config = {}
            ceph_osd_config['section'] = 'osd'
            ceph_osd_config['items'] = []
            ceph_mds_config = {}
            ceph_mds_config['section'] = 'mds'
            ceph_mds_config['items'] = []
            new_ceph_config = []
            new_ceph_config.append(ceph_global_config)
            new_ceph_config.append(ceph_mon_config)
            new_ceph_config.append(ceph_osd_config)
            new_ceph_config.append(ceph_mds_config)

        # print new_ceph_config
        context["config_list"] = new_ceph_config
        return context

class CreateView(forms.ModalFormView):
    form_class = CreateCephConfigForm
    template_name = 'vsm/ceph_config_mgmt/create.html'
    success_url = reverse_lazy('horizon:vsm:ceph_config_mgmt:index')

def create_ceph_config(request):
    data = json.loads(request.body)
    print "============create the configuration============="
    print data
    config_name = data['name']
    config_value = data['value']
    config_category = data['category']
    config_section = data['section']
    config_alterable = str(data['alterable'])
    config_description = data['description']
    try:
        vsmapi.config_create(request, config_name, config_value, config_category,
                             config_section, config_alterable, config_description)
        resp = dict(message="Succeed to create ceph config %s" % config_name,
                    status="OK", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
    except:
        resp = dict(message="Fail to create ceph config %s" % config_name,
                    status="Error", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)

def update_ceph_config(request, action):
    data = json.loads(request.body)
    print "============update the configuration============="
    print data
    config_id = data['config_id']
    config_section = data['config_section']
    config_current_value = data['config_value']
    config_description = data['config_description']
    try:
        vsmapi.config_update(request, config_id, config_section,
                             config_current_value, config_description)
        resp = dict(message="Succeed to update ceph config", status="success", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
    except:
        resp = dict(message="Fail to update ceph config", status="error", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)


def delete_ceph_config(request):
    data = json.loads(request.body)
    print "============delete the configuration============="
    print data
    try:
        for config_id in data:
            print config_id
            vsmapi.config_delete(request, config_id)
        resp = dict(message="Succeed to delete ceph config", status="OK", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
    except:
        resp = dict(message="Fail to delete ceph config", status="Error", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)

def detect_ceph_config(request):
    try:
        vsmapi.config_detect(request)
        resp = dict(message="Succeed to detect ceph config", status="OK", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
    except:
        resp = dict(message="Fail to detect ceph config", status="Error", data="")
        resp = json.dumps(resp)
        return HttpResponse(resp)
