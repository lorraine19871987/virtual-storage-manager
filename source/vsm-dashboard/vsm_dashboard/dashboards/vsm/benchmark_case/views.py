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
from django.shortcuts import render

from horizon import tables

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
                "runtime": bm_case.runtime,
                "running_hosts": bm_case.running_hosts,
                "status": bm_case.status
            }
            case_list.append(case)

        return case_list


def add_benchmark_case_view(request):
    template = "vsm/benchmark_case/add_benchmark_case.html"
    context = {}
    context["ioengine"] = [('rbd', "rbd")]
    context["readwrite"] = [('read', "read"),
                            ('write', "write"),
                            ('rw', "rw"),
                            ('randread', "randread"),
                            ('randwrite', "randwrite"),
                            ('randrw', "randrw")]
    return render(request, template, context)

def add_benchmark_case(request):
    data = json.loads(request.body)
    print data
    name = data['name']
    readwrite = data['readwrite']
    blocksize = data['blocksize']
    iodepth = data['iodepth']
    runtime = data['runtime']
    ioengine = data['ioengine']
    clientname = data['clientname']
    additional_options = data['additional_options']

    ret = {'error_code': 0, 'error_msg':''}
    try:
        vsmapi.benchmark_case_create(request, name, readwrite, blocksize, iodepth,
                                     runtime, ioengine, clientname, additional_options)
    except:
        ret = {'error_code': -1,'error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def run_benchmark_case_view(request):
    template = "vsm/benchmark_case/run_benchmark_case.html"
    servers = vsmapi.get_server_list(None, )
    context = {}
    cases = vsmapi.benchmark_case_get_all(request)
    flag = 0
    is_running_hosts = []
    for case in cases:
        if case.status == "running":
            cases.pop(flag)
            running_hosts = case.running_hosts
            is_running_hosts.extend(running_hosts.split(","))
            continue
        flag += 1
    flag = 0
    for server in servers:
        if server.host in is_running_hosts:
            servers.pop(flag)
            continue
        flag += 1
    context["cases"] = cases
    context["servers"] = servers
    pools = vsmapi.pool_status(None)
    context["pool_list"] = [(pool.name, pool.name) for pool in pools if not pool.cache_tier_status]
    return render(request, template, context)

def run_benchmark_case(request):
    data = json.loads(request.body)
    print data
    case_id = data['caseId']
    host = data['host']
    pool = data['pool']
    rbd_num = data['rbd_num']
    rbd_size = data['rbd_size']

    body = {
        "benchmark_info": [
            {
                "host": host,
                "pool_rbd": [
                    {"pool": pool, "rbds": "", "rbd_num": int(rbd_num), "rbd_size": rbd_size}
                ]
            }
        ]
    }

    ret = {'error_code': 0, 'error_msg':''}
    try:
        vsmapi.benchmark_case_run(request, case_id, body)
    except:
        ret = {'error_code': -1,'error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def delete_benchmark_case(request):
    data = json.loads(request.body)
    case_id_list = data["case_id_list"]

    for case_id in case_id_list:
        vsmapi.benchmark_case_delete(request, case_id)

    rs = json.dumps({"status":0})
    return HttpResponse(rs)

def terminate_benchmark_case(request):
    data = json.loads(request.body)
    case_id_list = data["case_id_list"]

    for case_id in case_id_list:
        vsmapi.benchmark_case_terminate(request, case_id)

    rs = json.dumps({"status":0})
    return HttpResponse(rs)

def update_benchmark_list(request):
    cases = vsmapi.benchmark_case_get_all(request)
    case_list = []
    for _case in cases:
        case = {
            "id": _case.id,
            "name": _case.name,
            "ioengine": _case.ioengine,
            "readwrite": _case.readwrite,
            "runtime": _case.runtime,
            "running_hosts": _case.running_hosts,
            "status": _case.status
        }
        case_list.append(case)
    return HttpResponse(json.dumps(case_list))