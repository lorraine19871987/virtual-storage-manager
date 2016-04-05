
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
from .views import IndexView
from .views import delete_benchmark_case
from .views import terminate_benchmark_case
from .views import add_benchmark_case_view
from .views import run_benchmark_case_view
from .views import add_benchmark_case
from .views import run_benchmark_case
from .views import update_benchmark_list

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^delete_benchmark_case/$', delete_benchmark_case, name='delete_benchmark_case'),
    url(r'^terminate_benchmark_case/$', terminate_benchmark_case, name='terminate_benchmark_case'),
    url(r'^add_benchmark_case_view/$', add_benchmark_case_view, name='add_benchmark_case_view'),
    url(r'^run_benchmark_case_view/$', run_benchmark_case_view, name='run_benchmark_case_view'),
    url(r'^add_benchmark_case/$', add_benchmark_case, name='add_benchmark_case'),
    url(r'^run_benchmark_case/$', run_benchmark_case, name='run_benchmark_case'),
    url(r'^update_benchmark_list/$', update_benchmark_list, name='update_benchmark_list'),
)
