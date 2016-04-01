# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.
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

from vsm.api import common
import logging

LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = "benchmark_cases"

    def show(self, request, benchmark_case, brief=False):
        benchmark_case_dict = dict(
            id=benchmark_case.get('id'),
            name=benchmark_case.get('name'),
            readwrite=benchmark_case.get('readwrite'),
            blocksize=benchmark_case.get('blocksize'),
            iodepth=benchmark_case.get('iodepth'),
            runtime=benchmark_case.get('runtime'),
            ioengine=benchmark_case.get('ioengine'),
            clientname=benchmark_case.get('clientname'),
            additional_options=benchmark_case.get('additional_options'),
            status=benchmark_case.get('status'),
            running_hosts=benchmark_case.get('running_hosts')
        )
        if brief:
            return benchmark_case_dict
        else:
            return dict(benchmark_case=benchmark_case_dict)

    def index(self, request, benchmark_cases):
        benchmark_case_list = [self.show(request, benchmark_case, True)
                       for benchmark_case in benchmark_cases]
        return dict(benchmark_cases=benchmark_case_list)