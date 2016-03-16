#  Copyright 2014 Intel Corporation, All Rights Reserved.
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

"""
RBDSnapShot interface.
"""

import urllib
from vsmclient import base


class RBDSnapShot(base.Resource):
    """A RBDSnapShot is an extra block level storage to the OpenStack instances."""
    def __repr__(self):
        return "<RBDSnapShot: %s>" % self.id

class RBDSnapShotsManager(base.ManagerWithFind):
    """
    Manage :class:`RBDSnapShot` resources.
    """
    resource_class = RBDSnapShot



    def list(self, detailed=False, search_opts=None, paginate_opts=None):
        """
        Get a list of all RBDSnapShot.

        :rtype: list of :class:`RBDSnapShot`
        """
        if search_opts is None:
            search_opts = {}

        if paginate_opts is None:
            paginate_opts = {}

        qparams = {}

        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        for opt, val in paginate_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        detail = ""
        if detailed:
            detail = "/detail"

        ret = self._list("/snapshots%s%s" % (detail, query_string),
                          "snapshots")
        return ret


    def rbd_snapshot_create(self, body):
        '''
        :param request:
        :param body:{'snapshots':[
                            {'pool':,#pool_id
                            'image':,#image_id
                            'size' :1024,#MB
                            'name':'snapshot_name1',#},
                            ]
                    }
        :return:
        '''
        url = '/snapshots/rbd_snapshot_create'
        return self.api.client.post(url, body=body)

    def rbd_snapshot_remove(self, body):
        '''
        :param request:
        :param body:{'snapshots':[2,]}
        :return:
        '''
        url = '/snapshots/rbd_snapshot_remove'
        return self.api.client.post(url, body=body)

