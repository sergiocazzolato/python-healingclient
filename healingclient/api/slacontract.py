# -*- coding: utf-8 -*-
#
# Copyright 2014 - Intel
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

from healingclient.api import base


class SLAContract(base.Resource):
    resource_name = 'SLAContract'


class SLAContractManager(base.ResourceManager):
    resource_class = SLAContract

    def create(self, tenant_id=None, type=None, value=None, action=None):
        self._ensure_not_empty(name=type)
        self._ensure_not_empty(name=action)

        data = {
            'tenant_id': tenant_id,
            'type': type,
            'value': value,
            'action': action
        }

        return self._create('/sla/contract', data)

    def update(self, id, tenant_id=None, type=None, value=None, action=None):
        self._ensure_not_empty(name=id)
        self._ensure_not_empty(name=type)
        self._ensure_not_empty(name=action)

        data = {
            'id': id,
            'tenant_id': tenant_id,
            'type': type,
            'value': value,
            'action': action
        }

        return self._update('/sla/contract/%s' % id, data)

    def list(self):
        return self._list('/sla/contract', 'slacontracts')

    def get(self, id):
        self._ensure_not_empty(name=id)

        return self._get('/sla/contract/%s' % id)

    def delete(self, id):
        self._ensure_not_empty(name=id)

        self._delete('/sla/contract/%s' % id)
