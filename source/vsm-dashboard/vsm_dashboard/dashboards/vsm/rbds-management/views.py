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

@csrf_exempt
def clone_rbd_view(request):
    template = "vsm/rbds-management/clone_rbd.html"
    context = {}
    ret = render(request,template,context)
    return ret

def clone_rbd(request):
    body = json.loads(request.body)
    try:
        rsp, ret = vsmapi.rbd_clone(request,body=body)
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
    body = json.loads(request.body)
    try:
        print '888===',body
        rsp, ret = vsmapi.rbd_snapshot_rollback(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def get_image_formt(request):
    image_formt_list = [(1,'default'),(2,'supports cloning')]
    resp = json.dumps({"image_formt_list":image_formt_list})
    return HttpResponse(resp)

def list_rbds_by_pool(request):
    rbd_list = []
    pool_name = request.GET.get("pool_name", None)
    rbd_format = request.GET.get("rbd_format", None)
    if pool_name is None:
        pool_id = int(request.GET.get("pool_id", None))
        rsp, pool_objs = vsmapi.pools_list(request)
        pool_obj = [pool['name'] for pool in pool_objs['pool'] if pool['pool_id'] == pool_id ]
        pool_name = pool_obj[0]
    rbd_obj_list= vsmapi.rbd_pool_status(request)
    for rbd in rbd_obj_list:
        if rbd.pool == pool_name:
            if rbd_format is not None and rbd.format != rbd_format:
                pass
            else:
                rbd_list.append((rbd.id,rbd.image_name))
    resp = json.dumps({"rbd_list":rbd_list})
    return HttpResponse(resp)

def list_snapshots_by_image(request):
    snapshot_list = []
    rbd_id = int(request.GET.get("rbd_id",None))
    rbd_obj_list= vsmapi.rbd_pool_status(request)
    for rbd in rbd_obj_list:
        if rbd.id == rbd_id:
            rsp, snapshots = vsmapi.snapshot_get_by_image(request,{'rbd_id':rbd_id})
            snapshots = snapshots['snapshots']
            print '444==',snapshots
            for snap in snapshots:
                snapshot_list.append((snap['id'],snap['name']))
            print '999===',snapshot_list
            # if rbd.parent_snapshot:
            #     snapshot_list.append(('',rbd.parent_snapshot))#TODO
            break
    resp = json.dumps({"snapshot_list":snapshot_list})
    return HttpResponse(resp)
