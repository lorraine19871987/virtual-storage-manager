
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
from .views import IndexView,add_snapshot_view,add_snapshot,\
    remove_snapshots

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add_snapshot_view/$', add_snapshot_view, name='add_snapshot_view'),
    url(r'^add_snapshot/$', add_snapshot, name='add_snapshot'),
    url(r'^remove_snapshots/$', remove_snapshots, name='remove_snapshots'),

)

