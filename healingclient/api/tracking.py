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


class Tracking(base.Resource):
    resource_name = 'Tracking'


class TrackingManager(base.ResourceManager):
    resource_class = Tracking

    def list(self):
        return self._list('/sla/tracking', 'failures')

    def create(self, created_at, alarm_id, data=None):
        self._ensure_not_empty(created_at=created_at)
        self._ensure_not_empty(alarm_id=alarm_id)

        data = {
            'created_at': created_at,
            'alarm_id': alarm_id,
            'data': data
        }
        self._create('/sla/tracking', data)

