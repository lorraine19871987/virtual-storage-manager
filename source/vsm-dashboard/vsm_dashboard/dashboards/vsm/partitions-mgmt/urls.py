
# Copyright 2014 Intel Corporation, All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the"License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

from django.conf.urls import patterns, url
from .views import mgmt_parts_views
from .views import mgmt_parts_action,get_disks_by_server,get_parts_by_disk


urlpatterns = patterns('',
    url(r'^$', mgmt_parts_views, name='index'),
    url(r'^get_disks_by_server/$', get_disks_by_server, name='get_disks_by_server'),
    url(r'^get_parts_by_disk/$', get_parts_by_disk, name='get_parts_by_disk'),
    url(r'^mgmt_parts_views/$', mgmt_parts_views, name='mgmt_parts_views'),
    url(r'^mgmt_parts_action/$', mgmt_parts_action, name='mgmt_parts_action'),
)
