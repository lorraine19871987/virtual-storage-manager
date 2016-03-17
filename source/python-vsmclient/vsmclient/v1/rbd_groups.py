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
RBDGroup interface.
"""

import urllib
from vsmclient import base


class RBDGroup(base.Resource):
    """A RBDGroup is an extra block level storage to the OpenStack instances."""
    def __repr__(self):
        return "<RBDGroup: %s>" % self.id

class RBDGroupsManager(base.ManagerWithFind):
    """
    Manage :class:`RBDGroup` resources.
    """
    resource_class = RBDGroup



    def list(self, detailed=False, search_opts=None, paginate_opts=None):
        """
        Get a list of all RBDGroup.

        :rtype: list of :class:`RBDGroup`
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

        ret = self._list("/rbd_groups%s%s" % (detail, query_string),
                          "rbd_groups")
        return ret


    def rbd_group_create(self, body):
        '''
        :param request:
        :param body:{'rbd_groups':[
                            {'name':,#
                            'comments':,#
                            ]
                    }
        :return:
        '''
        url = '/snapshots/rbd_group_create'
        return self.api.client.post(url, body=body)

    def rbd_group_update(self, body):
        '''
        :param request:
        :param body:{'rbd_groups':[
                            {'name':,#
                            'comments':,#
                            'id':,
                            ]
                    }
        :return:
        '''
        url = '/snapshots/rbd_group_update'
        return self.api.client.post(url, body=body)

    def rbd_group_remove(self, body):
        '''
        :param request:
        :param body:{'rbd_groups':[2,]}
        :return:
        '''
        url = '/snapshots/rbd_group_remove'
        return self.api.client.post(url, body=body)

