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

import urllib

from healingclient.api import base


class SLAStatistics(base.Resource):
    resource_name = 'statistics'


class SLAStatisticsManager(base.ResourceManager):
    resource_class = SLAStatistics

    def get(self, stat_type, project_id, from_date, to_date,
            resource_id=None):
        self._ensure_not_empty(project_id=project_id)

        data = dict()
        data['stat_type'] = stat_type
        data['project_id'] = project_id
        data['from_date'] = from_date
        data['to_date'] = to_date
        if resource_id:
            data['resource_id'] = resource_id
        query = urllib.urlencode(data)

        return self._get('/sla/statistics?%s' % query)
