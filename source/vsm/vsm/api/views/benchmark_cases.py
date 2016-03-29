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

    # def show(self, request, config, brief=False):
    #     config_dict = dict(
    #         id=config.get('id'),
    #         name=config.get('name'),
    #         value=config.get('value'),
    #         default_value=config.get('default_value'),
    #         category=config.get('category'),
    #         section=config.get('section'),
    #         description=config.get('description'),
    #         alterable=config.get('alterable')
    #     )
    #     if brief:
    #         return config_dict
    #     else:
    #         return dict(config=config_dict)
    #
    # def index(self, request, configs):
    #     config_list = [self.show(request, config, True)
    #                    for config in configs]
    #     return dict(configs=config_list)