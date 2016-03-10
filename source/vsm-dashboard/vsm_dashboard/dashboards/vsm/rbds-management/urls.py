
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
from .views import IndexView,create_new_rbd,create_new_rbd_view, \
    remove_rbds,flatten_rbds,get_image_formt,rollback_snapshot_view,\
    create_snapshot,create_snapshot_view,list_rbds_by_pool,\
    list_snapshots_by_image,rollback_snapshot,clone_rbd,clone_rbd_view


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create_new_rbd/$', create_new_rbd, name='create_new_rbd'),
    url(r'^remove_rbds/$', remove_rbds, name='remove_rbds'),
    url(r'^clone_rbd_view/$', clone_rbd_view, name='clone_rbd_view'),
    url(r'^clone_rbd/$', clone_rbd, name='clone_rbd'),
    url(r'^flatten_rbds/$', flatten_rbds, name='flatten_rbds'),
    url(r'^get_image_formt/$', get_image_formt, name='get_image_formt'),
    # url(r'^devices/(?P<action>\w+)$', DevicesAction, name='devicesaction'),
    url(r'^create_new_rbd_view/$', create_new_rbd_view, name='create_new_rbd_view'),
    url(r'^list_snapshots_by_image/$', list_snapshots_by_image, name='list_snapshots_by_image'),
    url(r'^rollback_snapshot/$', rollback_snapshot, name='rollback_snapshot'),
    url(r'^rollback_snapshot_view/$', rollback_snapshot_view, name='rollback_snapshot_view'),
    url(r'^create_snapshot_view/$', create_snapshot_view, name='create_snapshot_view'),
    url(r'^create_snapshot/$', create_snapshot, name='create_snapshot'),
    url(r'^list_rbds_by_pool/$', list_rbds_by_pool, name='list_rbds_by_pool'),
    url(r'/', IndexView.as_view(), name='index'),
)

