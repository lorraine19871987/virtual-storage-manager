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
from vsm_dashboard.api import vsm as vsmapi
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import json
LOG = logging.getLogger(__name__)

FORMAT_TYPES = ['--','xfs','ext4']

@csrf_exempt
def mgmt_parts_views(request):
    template = "vsm/partitions-mgmt/parts_mgmt.html"
    context = {}
    servers = vsmapi.get_server_list(None, )
    print 'servers====%s'%servers
    context["servers"] = servers
    server_id = servers[0].id
    print '11111,---',server_id
    resp,disks = vsmapi.get_disks_by_server(request,{"server_id":server_id})
    print '2222,---',disks
    disk_name = disks['disks'][0]['name']
    context["disks"] = disks['disks']
    disk_condition  = {"server_id":server_id,
                       "disk_name":disk_name,
                       }
    print '333--',disk_condition
    resp,parts = vsmapi.get_parts_by_disk(request,disk_condition)
    context["parts"] = parts['parts']
    context["format_types"] = FORMAT_TYPES
    print '4444--',parts
    return render(request,template,context)


def mgmt_parts_action(request):
    """ body = {'server_id':1,'disk_name':'/dev/vdb',
    to_remove:[{'number':2}],to_add:[{}],to_format:[{'number':'1',new_format:"xfs"}]
    }"""
    body = json.loads(request.body)
    try:
        rsp, ret = vsmapi.mgmt_partition_for_disk(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def get_disks_by_server(request):
    body = json.loads(request.body)
    resp_code,disks = vsmapi.get_disks_by_server(request,body=body)
    resp = json.dumps(disks['disks'])
    return HttpResponse(resp)

def get_parts_by_disk(request):
    body = json.loads(request.body)
    resp_code,parts = vsmapi.get_parts_by_disk(request,body=body)
    resp = json.dumps(parts['parts'])
    return HttpResponse(resp)





