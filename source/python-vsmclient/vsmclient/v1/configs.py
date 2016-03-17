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
Config interface (1.1 extension).
"""

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import six
from vsmclient import base

class Config(base.Resource):
    """A config is a config management to the vsm instances."""
    def __repr__(self):
        return "<CONFIG: %s>" % self.id

    def delete(self):
        """Delete this config."""
        self.manager.delete(self)

    def update(self, **kwargs):
        """Update the value or description for this config."""
        self.manager.update(self, **kwargs)


class ConfigsManager(base.ManagerWithFind):
    """
    Manage :class:`CONFIG` resources.
    """
    resource_class = Config

    def get(self, config_id):
        """
        Get a config.

        :param config_id: The ID of the config.
        :rtype: :class:`CONFIG`
        """
        return self._get("/configs/%s" % config_id, "config")

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all configs.

        :rtype: list of :class:`CONFIG`
        """
        if search_opts is None:
            search_opts = {}

        qparams = {}

        for opt, val in six.iteritems(search_opts):
            if val:
                qparams[opt] = val

        # Transform the dict to a sequence of two-element tuples in fixed
        # order, then the encoded string will be consistent in Python 2&3.
        if qparams:
            new_qparams = sorted(qparams.items(), key=lambda x: x[0])
            query_string = "?%s" % urlencode(new_qparams)
        else:
            query_string = ""

        detail = ""
        if detailed:
            detail = "/detail"

        return self._list("/configs%s%s" % (detail, query_string),
                          "configs")

    def create(self, name, value, category, section, alterable, description=None):
        """
        Create a config.

        :param name: Name of config
        :param value: Value of config
        :param category: Category of config, CEPH or VSM
        :param section: Section of config, if category is CEPH, the section is a list of
            global, osd, mds or mon
        :param alterable: Alterable of config
        :param description: Description of config
        :rtype: :class:`Config`
        """

        body = {'config': {'name': name,
                           'value': value,
                           'category': category,
                           'section': section,
                           'alterable': alterable,
                           'description': description
                           }}
        return self._create('/configs', body, 'config')

    def delete(self, config):
        self._delete("/configs/%s" % base.getid(config))

    def update(self, config, **kwargs):
        """
        Update the name or description for a config.

        :param config: The :class:`Config` to update.
        """
        if not kwargs:
            return

        body = {"config": kwargs}

        self._update("/configs/%s" % base.getid(config), body)

    def detect(self):
        """Detect the configs from ceph.conf"""

        self.api.client.post("/configs/detect")