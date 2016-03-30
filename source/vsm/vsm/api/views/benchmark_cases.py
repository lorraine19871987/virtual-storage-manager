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
            direct=benchmark_case.get('direct'),
            time_based=benchmark_case.get('time_based'),
            readwrite=benchmark_case.get('readwrite'),
            blocksize=benchmark_case.get('blocksize'),
            iodepth=benchmark_case.get('iodepth'),
            ramp_time=benchmark_case.get('ramp_time'),
            runtime=benchmark_case.get('runtime'),
            ioengine=benchmark_case.get('ioengine'),
            clientadmin=benchmark_case.get('clientadmin'),
            iodepth_batch_submit=benchmark_case.get('iodepth_batch_submit'),
            iodepth_batch_complete=benchmark_case.get('iodepth_batch_complete'),
            norandommap=benchmark_case.get('norandommap'),
            randrepeat=benchmark_case.get('randrepeat'),
            rate_iops=benchmark_case.get('rate_iops'),
            random_distribution=benchmark_case.get('random_distribution'),
            rate=benchmark_case.get('rate'),
            rwmixread=benchmark_case.get('rwmixread'),
            additional_options=benchmark_case.get('additional_options'),
            status=benchmark_case.get('status'),
        )
        if brief:
            return benchmark_case_dict
        else:
            return dict(benchmark_case=benchmark_case_dict)
    #
    # def index(self, request, configs):
    #     config_list = [self.show(request, config, True)
    #                    for config in configs]
    #     return dict(configs=config_list)