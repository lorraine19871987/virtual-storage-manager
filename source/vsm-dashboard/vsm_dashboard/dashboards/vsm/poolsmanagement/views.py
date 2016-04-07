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
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.core import urlresolvers
from horizon import exceptions
from horizon import tables
from horizon import forms

from vsm_dashboard.api import vsm as vsmapi
from .form import CreateErasureCodedPool
from .form import RemoveCacheTier,CreatePoolSnapshot
from .tables import ListPoolTable

from vsm_dashboard.api import vsm as vsmapi
import json
from django.http import HttpResponse

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = ListPoolTable
    template_name = 'vsm/poolsmanagement/index.html'

    def get_data(self):
        pools = []

        try:
            rsp, body = vsmapi.pools_list(self.request, all_pools=True)
            if body:
                pools = body["pool"]
            logging.debug("resp body in view: %s" % pools)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve storage pool list. '))
        pools = sorted(pools, lambda x,y: cmp(x['poolId'], y['poolId']))
        #pools = [pool for pool in pools if pool['tag'] != "SYSTEM"]
        return pools

class CreateView(TemplateView):
    template_name = 'vsm/poolsmanagement/create_replicated_pool.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context["sg_list"] = []
        return context

class CreateErasureCodedPoolView(forms.ModalFormView):
    form_class = CreateErasureCodedPool
    template_name = 'vsm/poolsmanagement/create_erasure_coded_pool.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')

class AddCacheTierView(TemplateView):
    template_name = 'vsm/poolsmanagement/add_cache_tier.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')

    def get_context_data(self, **kwargs):
        context = super(AddCacheTierView, self).get_context_data(**kwargs)
        #get pool list
        pools = vsmapi.pool_status(None)
        context["pool_list"] = [(pool.pool_id, pool.name) for pool in pools if not pool.cache_tier_status]
        context["cache_mode_list"] = [('writeback', "Writeback"), ('readonly', "Read-only")]
        context["hit_set_type_list"] = [('bloom', "bloom")]
        # get vsm configs
        vsm_configs = vsmapi.config_get_all(None, search_opts={"category": "VSM"})
        context["settings"] = dict([(config.name, config.value) for config in vsm_configs])
        return context


class RemoveCacheTierView(forms.ModalFormView):
    form_class = RemoveCacheTier
    template_name = 'vsm/poolsmanagement/remove_cache_tier.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')

class CPPoolView(TemplateView):
    template_name = 'vsm/poolsmanagement/cp_pool.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')

    def get_context_data(self, **kwargs):
        context = super(CPPoolView, self).get_context_data(**kwargs)
        #get pool list
        pools = vsmapi.pool_status(None)
        context["pool_list"] = [(pool.pool_id, pool.name) for pool in pools if not pool.cache_tier_status]
        return context

def add_cache_tier(request):
    status = ""
    msg = ""
    body = json.loads(request.body)

    try:
        ret = vsmapi.add_cache_tier(request,body=body)
        status = "OK"
        msg = "Add Cache Tier Successfully!"
    except:
        status = "Failed"
        msg = "Add Cache Tier Failed!"

    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)


def remove_cache_tier(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    try:
        ret = vsmapi.remove_cache_tier(request,body=body)
        status = "OK"
        msg = "Remove Cache Tier Successfully!"
    except:
        status = "Failed"
        msg = "Remove Cache Tier Failed!"

    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)


def create_replicated_pool(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.create_storage_pool(request,body=body)
        res = str(ret['message']).strip()
        if res.startswith('pool') and res.endswith('created'):
            status = "OK"
            msg = "Created storage pool successfully!"
    except:
        status = "Failed"
        msg = "Create Replication Pool Failed!"
    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

def create_ec_pool(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body

    try:
        rsp, ret = vsmapi.create_storage_pool(request,body=body)
        res = str(ret['message']).strip()
        if res.startswith('pool') and res.endswith('created'):
            status = "OK"
            msg = "Created storage pool successfully!"
    except:
        status = "Failed"
        msg = "Remove Cache Tier Failed!"

    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

def cp_pool(request):
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.cp_pool(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def remove_pools(request):
    data = json.loads(request.body)
    storage_pool_id_list = data["storage_pool_id_list"]
    storage_pools = {'storage_pools':storage_pool_id_list}
    try:
        rsp, ret = vsmapi.remove_pools(request, storage_pools)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)


def get_default_pg_number_storage_group(request):
    storage_group_list = []
    rsp, group_list= vsmapi.get_storage_group_list(request)
    for key in group_list:
        rsp, default_pg_num = vsmapi.get_default_pg_num_by_storage_group(request, \
                                                   {'storage_group_name':group_list[key]})
        if default_pg_num['pg_num_default'] > 0:
            storage_group_list.append((key, group_list[key], default_pg_num['pg_num_default']))
    resp = json.dumps({"storage_group_list":storage_group_list})
    return HttpResponse(resp)

def list_pools_for_sel_input(request):
    pool_list = []
    storage_pool_list= vsmapi.pool_list(request)
    for pool in storage_pool_list:
        pool_list.append((pool['pool_id'],pool['name']))
    resp = json.dumps({"pool_list":pool_list})
    return HttpResponse(resp)

class CreatPoolSnapshotView(forms.ModalFormView):
    form_class = CreatePoolSnapshot
    form_id = "create_snapshot_form"
    modal_id = "create_snapshot_modal"
    modal_header = _("Create An Pool SnapShot")
    submit_label = _("Create Snap")
    submit_url = reverse_lazy('horizon:vsm:poolsmanagement:create_pool_snap')
    template_name = 'vsm/poolsmanagement/create_pool_snap.html'
    success_url = reverse_lazy("horizon:vsm:poolsmanagement:index")
    page_title = _("Create An Pool SnapShot")

    def get_object(self):
        try:
            return self.kwargs["pool_id"]
        except Exception:
            pass

    def get_initial(self):
        print 'self.kwargs---',self.kwargs
        return {"pool_id": self.kwargs["pool_id"]}

    def get_context_data(self, **kwargs):
        context = super(CreatPoolSnapshotView, self).get_context_data(**kwargs)
        context['pool'] = self.get_object()
        args = (self.kwargs['pool_id'],)
        #context['submit_url'] = urlresolvers.reverse(self.submit_url, args=args)
        return context