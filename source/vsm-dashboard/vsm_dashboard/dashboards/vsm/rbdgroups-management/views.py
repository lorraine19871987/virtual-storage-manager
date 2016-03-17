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
from .tables import SnapshotsTable
from django.http import HttpResponse,HttpResponseRedirect
from vsm_dashboard.utils import get_time_delta
import json
LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = SnapshotsTable
    template_name = 'vsm/snapshots-management/index.html'

    def get_data(self):
        _snap_status = []
        try:
            _snap_status = vsmapi.snapshot_get_all(self.request)
            print '_snap_status===%s'%_snap_status
            if _snap_status:
                logging.debug("resp body in view: %s" % _snap_status)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve sever list. '))

        snap_status = []
        for _snap in _snap_status:
            snap = {
                      "id": _snap.id,
                      "snapshot_name":_snap.name,
                      "pool": _snap.pool,
                      "image_name": _snap.image,
                      "created_at": _snap.created_at,
                      "snap_id": _snap.snap_id,
                      "status": _snap.status,
                      "size": _snap.size,
                      }

            snap_status.append(snap)
        return snap_status



def add_rbd_group_view(request):
    print '222222222'
    template = "vsm/rbd_groups-management/add_rbd_group.html"
    context = {}
    return render(request,template,context)

def add_rbd_group(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.rbd_group_create(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def remove_rbd_groups(request):
    data = json.loads(request.body)
    rbd_group_id_list = data["rbd_group_id_list"]

    rbd_groups = {'rbd_groups':rbd_group_id_list}
    print '---rbd_groups remove-%s'%rbd_groups
    #ret,message = vsmapi.rbd_remove(request, rbds)
    try:
        rsp, ret = vsmapi.rbd_group_remove(request, rbd_groups)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)