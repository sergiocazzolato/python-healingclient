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
import six
from healingclient.api import base


class Action(base.Resource):
    resource_name = 'Action'


class ActionManager(base.ResourceManager):
    resource_class = Action

    def list(self, request_id=None, name=None):
        params = {}
        if name:
            params['name'] = name
        elif request_id:
            params['request_id'] = request_id
        
        return self._list('?'.join(['/sla/actions', 
                                    six.moves.urllib.parse.urlencode(params)]),
                          'actions')

    def create(self, name, target_id, request_id, status, created_at=None,
               output=None):
        self._ensure_not_empty(name=name)
        self._ensure_not_empty(target_id=target_id)
        self._ensure_not_empty(request_id=request_id)
        self._ensure_not_empty(status=status)

        data = {
            'name': name,
            'target_id': target_id,
            'request_id': request_id,
            'created_at': created_at,
            'status': status,
            'output': output
        }
        self._create('/sla/actions', data)
