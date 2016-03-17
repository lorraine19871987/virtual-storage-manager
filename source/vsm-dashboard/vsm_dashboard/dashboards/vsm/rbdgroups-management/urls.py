
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
from .views import IndexView,add_rbd_group_view,add_rbd_group,\
    remove_rbd_groups

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add_rbd_group_view/$', add_rbd_group_view, name='add_rbd_group_view'),
    url(r'^add_rbd_group/$', add_rbd_group, name='add_rbd_group'),
    url(r'^remove_rbd_groups/$', remove_rbd_groups, name='remove_rbd_groups'),

)
