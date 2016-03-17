
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


from django.utils.translation import  ugettext_lazy as _

from horizon import forms


class UpdateVSMConfigForm(forms.SelfHandlingForm):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    default_value = forms.CharField(
        label=_("Default Value"),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    value = forms.CharField(label=_("Value"), required=True)
    description = forms.CharField(label=_("Description"), required=False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateVSMConfigForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        pass
