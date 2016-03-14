# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.

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

"""The configs api."""


import webob
from webob import exc

from vsm.api.openstack import wsgi
from vsm.api.views import configs as config_views
from vsm import conductor
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm.openstack.common import timeutils
from vsm import scheduler

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS


def _convert_config_for_display(config):
    config['id'] = config['id']
    config['value'] = str(config['value'])
    config['default_value'] = str(config['default_value'])

    # convert 1 to True, 0 to False
    if config.get('alterable') == 1 or \
                    str(config.get('alterable')).lower == "true" or \
                    config.get('alterable') == "1":
        config['alterable'] = True
    elif config.get('alterable') == 0 or \
                    str(config.get('alterable')).lower == "false" or \
                    config.get('alterable') == "0":
        config['alterable'] = False
    else:
        raise exception.ConfigParameterValueError(parameter="alterable")
    # remove "_" if category is CEPH
    # remove "\" if it is before the "$"
    if config.get('category') == "CEPH":
        config['name'] = " ".join(config.get('name').split("_"))
        value = config.get('value')
        default_value = config.get('default_value')
        # config['value'] = "$".join(value.split("\$"))
        # config['default_value'] = "$".join(default_value.split("\$"))
    return config

def _convert_config_for_db(config):
    config['value'] = str(config['value'])
    config['default_value'] = str(config['default_value'])

    alterable = config.get('alterable', '')
    if str(alterable).lower() == "false":
        config['alterable'] = "0"
    elif str(alterable).lower() == "true":
        config['alterable'] = "1"

    if config.get('category') == "CEPH":
        config['name'] = "_".join(config.get('name').split(" "))
        # value = config.get('value')
        # default_value = config.get('default_value')
        # if "$" in value:
        #     config['value'] = "\$".join(value.split("$"))
        # if "$" in default_value:
        #     config['default_value'] = "\$".join(default_value.split("$"))
    return config


class ConfigController(wsgi.Controller):
    """The Config API controller for the VSM API."""

    _view_builder_class = config_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr
        super(ConfigController, self).__init__()


    def show(self, req, id):
        """Return data about the given config."""

        LOG.info("Show config data by config id")
        context = req.environ['vsm.context']

        try:
            config = self.conductor_api.config_get(context, id)
        except exception.NotFound:
            raise exc.HTTPNotFound()

        _convert_config_for_display(config)
        return self._view_builder.show(req, config)


    def index(self, req):
        """Returns the list of configs."""
        LOG.info("Get a list of configs")
        return self._items(req, entity_maker=self._view_builder.index)

    def _items(self, req, entity_maker):
        """Returns a list of configs."""

        filters = req.GET.copy()
        limit = filters.pop('limit', None)
        marker = filters.pop('marker', None)
        sort_key = filters.pop('sort_key', None)
        sort_dir = filters.pop('sort_dir', None)

        context = req.environ['vsm.context']

        search_opts = {}
        deleted = filters.pop('deleted', None)
        category = filters.pop('category', None)
        section = filters.pop('section', None)
        name = filters.pop('name', None)
        if not deleted or deleted.lower() == "false" or deleted == "0":
            search_opts["deleted"] = 0
        elif deleted.lower() == "true" or deleted == "1":
            search_opts["deleted"] = 1
        else:
            LOG.warning("deleted filter parameter is not correct")
        if category:
            search_opts["category"] = category
        if section:
            search_opts["section"] = section
        if name:
            search_opts["name"] = name

        LOG.info("Search_opts is " + str(search_opts))
        configs = self.conductor_api.config_get_all(context, marker=marker,
                                                    limit=limit,
                                                    sort_key=sort_key,
                                                    sort_dir=sort_dir,
                                                    filters=search_opts)

        for config in configs:
            _convert_config_for_display(config)
        return entity_maker(req, configs)

    def create(self, req, body):
        """Create a config."""
        context = req.environ['vsm.context']

        if not body:
            raise exc.HTTPUnprocessableEntity()

        if 'config' not in body:
            raise exc.HTTPUnprocessableEntity()

        config = body['config']

        category = config.get('category')
        if category != "CEPH":
            if category == "VSM":
                raise exception.ConfigNotSupprtCreateWithCategoryVSM()
            raise exception.ConfigCategoryError(category=category)

        section = config.get('section')
        section_list = ['global', 'osd', 'mon', 'mds']
        if section not in section_list:
            if "." in section:
                sec = section.split(".")[0]
                if sec not in section_list:
                    raise exception.ConfigSectionError(section=section)
            else:
                raise exception.ConfigSectionError(section=section)

        if not config.get('name') or not config.get('value') or \
            not config.get('category') or not config.get('section') or \
            not config.get('alterable'):
            raise exception.ConfigRequiredParameterMiss()

        config['default_value'] = config['value']

        config = _convert_config_for_db(config)
        new_config = self.conductor_api.config_create(context, config)

        # config into ceph.conf and restart service or tell the runtime env
        if new_config.get('category') == "CEPH":
            new_config = _convert_config_for_display(new_config)
            try:
                self.scheduler_api.config_into_ceph_conf(context, new_config)
                self.scheduler_api.config_into_effect(context, new_config)
            except:
                d_config = self.conductor_api.config_get_by_name_and_section(context,
                                                                             config['name'],
                                                                             config['section'])
                self.conductor_api.config_delete(context, d_config)
                self.scheduler_api.config_out_ceph_conf(context, new_config)
                raise exc.HTTPBadRequest()

        return {'config': _convert_config_for_display(new_config)}

    def delete(self, req, id):
        """Delete a config by a given id."""
        context = req.environ['vsm.context']

        if not id:
            raise exc.HTTPUnprocessableEntity()

        try:
            config = self.conductor_api.config_get(context, id)
            self.conductor_api.config_delete(context, config)
            new_config = config.copy()
            new_config = _convert_config_for_display(new_config)
            try:
                self.scheduler_api.config_out_ceph_conf(context, new_config)
                new_config['value'] = new_config['default_value']
                self.scheduler_api.config_into_effect(context, new_config)
            except:
                c_config = {"name": config.get('name'),
                            "value": config.get('value'),
                            "default_value": config.get('default_value'),
                            "category": config.get('category'),
                            "description": config.get('description'),
                            "section": config.get('section'),
                            "alterable": config.get('alterable')}
                self.conductor_api.config_create(context, c_config)
                self.scheduler_api.config_into_ceph_conf(context, new_config)
                raise exc.HTTPBadRequest()
        except exception.NotFound:
            raise exc.HTTPNotFound()
        return webob.Response(status_int=202)

    def update(self, req, id, body):
        """Update a config."""
        context = req.environ['vsm.context']
        if not body:
            raise exc.HTTPUnprocessableEntity()

        if 'config' not in body:
            raise exc.HTTPUnprocessableEntity()

        config = body['config']
        update_dict = {}

        valid_update_keys = (
            'section',
            'value',
            'description'
        )

        for key in valid_update_keys:
            if key in config.keys():
                update_dict[key] = config[key]
            else:
                update_dict[key] = ""

        try:
            config = self.conductor_api.config_get(context, id)
            config_new = config.copy()
            config_new.update(update_dict)
            # before into db, convert config
            config_new = _convert_config_for_db(config_new)
            for key in valid_update_keys:
                if key in config_new.keys():
                    update_dict[key] = config_new[key]
                else:
                    update_dict[key] = ""
            now = timeutils.utcnow()
            update_dict['updated_at'] = now
            LOG.info("Config update dict: " + str(update_dict))

            config_name = config_new.get("name")
            if config_name in ['cpu_diamond_collect_interval',
                               'ceph_diamond_collect_interval']:
                LOG.info("Reconfig the diamond config and restart the diamond daemon")
                diamond_config = {"name": config_name,
                                  "value": config_new.get("value")}
                self.scheduler_api.reconfig_diamond(context, diamond_config)

            config_new = self.conductor_api.config_update(context, config, update_dict)
            if config.get('category') == "CEPH" and update_dict['value'] != "":
                try:
                    LOG.info("================config_new: %s" % config_new)
                    config_new = _convert_config_for_display(config_new)
                    self.scheduler_api.config_into_ceph_conf(context, config_new)
                    self.scheduler_api.config_into_effect(context, config_new)
                except:
                    u_config = {"value": config.get('value'),
                                "description": config.get('description'),
                                "section": config.get('section')}
                    LOG.info("===========failed to update, u_config: %s" % u_config)
                    self.conductor_api.config_update(context, config, u_config)
                    config = _convert_config_for_display(config)
                    self.scheduler_api.config_into_ceph_conf(context, config)
                    LOG.info("===========success to rollback")
                    raise exc.HTTPBadRequest()
        except exception.NotFound:
            raise exc.HTTPNotFound

        return {'config': _convert_config_for_display(config_new)}

    def detect(self, req):
        """Detect the ceph config from the ceph.conf and insert them into db."""
        context = req.environ['vsm.context']
        try:
            ceph_configs_dict = self.scheduler_api.get_ceph_config(context)
        except:
            raise exc.HTTPBadRequest
        configs = []
        for k, v in ceph_configs_dict.iteritems():
            for kk, vv in v.iteritems():
                try:
                    create_body = {"name": kk,
                                   "value": vv,
                                   "default_value": vv,
                                   "category": "CEPH",
                                   "section": k,
                                   "alterable": True,
                                   "description": kk}
                    new_config = _convert_config_for_db(create_body)
                    new_config = self.conductor_api.config_create(context, new_config)
                    configs.append(_convert_config_for_display(new_config))
                except exception.ConfigExist:
                    update_body = {"value": vv}
                    now = timeutils.utcnow()
                    update_body['updated_at'] = now
                    kk = "_".join(kk.split(" "))
                    old_config = self.conductor_api.\
                        config_get_by_name_and_section(context, kk, k)
                    new_config = old_config.copy()
                    new_config.update(update_body)
                    new_config = _convert_config_for_db(new_config)
                    new_config = \
                        self.conductor_api.config_update(context, old_config, new_config)
                    configs.append(_convert_config_for_display(new_config))

        return {'configs': configs}

def create_resource(ext_mgr):
    return wsgi.Resource(ConfigController(ext_mgr))
