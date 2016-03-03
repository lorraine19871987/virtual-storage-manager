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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django import forms as django_froms
from horizon import exceptions
from horizon import tables
from horizon import forms
from vsm_dashboard.api import vsm as vsmapi
from .tables import RBDsTable
from django.http import HttpResponse,HttpResponseRedirect
from vsm_dashboard.utils import get_time_delta
import json
LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = RBDsTable
    template_name = 'vsm/rbds-management/index.html'

    def get_data(self):
        default_limit = 100;
        default_sort_dir = "asc";
        default_sort_keys = ['id']
        marker = self.request.GET.get('marker', "")

        _rbd_status = []
        #_rbds= vsmapi.get_rbd_list(self.request,)
        try:
            _rbd_status = vsmapi.rbd_pool_status(self.request, paginate_opts={
                "limit": default_limit,
                "sort_dir": default_sort_dir,
                "marker":   marker,
            })

            if _rbd_status:
                logging.debug("resp body in view: %s" % _rbd_status)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve sever list. '))

        rbd_status = []
        for _rbd in _rbd_status:
            rbd = {
                      "id": _rbd.id,
                      "pool": _rbd.pool,
                      "image_name": _rbd.image_name,
                      "size": _rbd.size/(1024*1024),
                      "objects": _rbd.objects,
                      "order": _rbd.order,
                      "format": _rbd.format,
                      "updated_at": get_time_delta(_rbd.updated_at),
                      }

            rbd_status.append(rbd)
        return rbd_status


@csrf_exempt
def create_new_rbd_view(request):
    template = "vsm/rbds-management/create_rbd.html"
    context = {}
    ret = render(request,template,context)
    return ret

def create_new_rbd(request):
    body = json.loads(request.body)
    try:
        rsp, ret = vsmapi.rbd_add(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def remove_rbds(request):
    data = json.loads(request.body)
    rbd_id_list = data["rbd_id_list"]
    rbds = {'rbds':rbd_id_list}
    ret,message = vsmapi.rbd_remove(request, rbds)
    rs = json.dumps(message)
    return HttpResponse(rs)

def flatten_rbds(request):
    data = json.loads(request.body)
    rbd_id_list = data["rbd_id_list"]
    rbds = {'rbds':rbd_id_list}
    ret,message = vsmapi.rbd_flatten(request, rbds)
    rs = json.dumps(message)
    return HttpResponse(rs)

@csrf_exempt
def create_snapshot_view(request):
    template = "vsm/rbds-management/create_snapshot.html"
    context = {}
    return render(request,template,context)

def create_snapshot(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.rbd_snapshot_create(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

@csrf_exempt
def rollback_snapshot_view(request):
    template = "vsm/rbds-management/rollback_snapshot.html"
    context = {}
    return render(request,template,context)

def rollback_snapshot(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.rbd_snapshot_create(request,body=body)
        msg = str(ret['message']).strip()
    except:
        status = "Failed"
        msg = "Create Snapshot Failed!"
    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

def get_image_formt(request):
    image_formt_list = [(1,'default'),(2,'supports cloning')]
    resp = json.dumps({"image_formt_list":image_formt_list})
    return HttpResponse(resp)