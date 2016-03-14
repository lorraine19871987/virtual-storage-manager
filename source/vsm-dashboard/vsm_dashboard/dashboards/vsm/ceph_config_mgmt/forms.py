
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

import logging

from django.utils.translation import ugettext_lazy as _
from horizon import forms

from vsm_dashboard.api import vsm as vsm_api

LOG = logging.getLogger(__name__)


def _sorted_all_configs(request):
    ceph_config = vsm_api.config_get_all(request)
    if ceph_config:
        _ceph_config = []
        for config in ceph_config:
            if config.section != "":
                _ceph_config.append({
                    "section": config.section,
                    "category": config.category
                })
        ceph_config = _ceph_config
        sort_on = "section"
        decorated = [(dict_[sort_on], dict_) for dict_ in ceph_config]
        decorated.sort()
        ceph_config = [dict_ for (key, dict_) in decorated]
        return ceph_config
    return []

class CreateCephConfigForm(forms.SelfHandlingForm):
    failure_url = 'horizon:vsm:ceph_config_mgmt:index'

    name = forms.CharField(
        label=_("Name"),
        required=True
    )
    value = forms.CharField(
        label=_("Value"),
        required=True
    )
    category = forms.CharField(
        label=_("Category"),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=True
    )
    section = forms.ChoiceField(
        label=_("Section"),
        required=True
    )
    alterable = forms.BooleanField(
        label=_("Alterable"),
        initial=True,
        required=False
    )
    description = forms.CharField(
        label=_("Description"),
        required=False
    )

    def __init__(self, request, *args, **kwargs):
        super(CreateCephConfigForm, self).__init__(request, *args, **kwargs)
        self.fields['category'].initial = "CEPH"
        ceph_config = _sorted_all_configs(request)
        section_list = []
        for config in ceph_config:
            category = config['category']
            if category == "CEPH":
                section = config['section']
                if (section, _(section)) not in section_list:
                    section_list.append((section, _(section)))
        self.fields['section'].choices = section_list

    def handle(self, request, data):
        pass


class UpdateCephConfigForm(forms.SelfHandlingForm):
    failure_url = 'horizon:vsm:ceph_config_mgmt:index'

    id = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    section = forms.ChoiceField(
        label=_('Section'),
        required=True
    )
    default_value = forms.CharField(
        label=_("Default Value"),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    current_value = forms.CharField(
        label=_("Current Value"),
        max_length=255,
        required=True,
        error_messages={
            'required': _('This field is required.')}
    )
    description = forms.CharField(
        label=_("Description"),
        required=False
    )

    def __init__(self, request, *args, **kwargs):
        super(UpdateCephConfigForm, self).__init__(request, *args, **kwargs)
        ceph_config = _sorted_all_configs(request)
        section_list = []
        for config in ceph_config:
            category = config['category']
            if category == "CEPH":
                section = config['section']
                if (section, _(section)) not in section_list:
                    section_list.append((section, _(section)))
        self.fields['section'].choices = section_list

    def handle(self, request, data):
        pass
