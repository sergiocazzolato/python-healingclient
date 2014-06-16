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

from cliff.command import Command as BaseCommand
from cliff.lister import Lister as ListCommand
from cliff.show import ShowOne as ShowCommand

from healingclient.openstack.common import log as logging
from healingclient.api.tracking import TrackingManager

LOG = logging.getLogger(__name__)


def format(tracking=None):
    columns = (
        'ID',
        'Time',
        'Alarm ID',
        'data',
        'Contract Names',
    )

    if tracking:
        data = (
            tracking.id,
            tracking.created_at,
            tracking.alarm_id,
            tracking.data or '<none>',
            tracking.contract_names or '<none>'
        )
    else:
        data = []

    return columns, data


class List(ListCommand):
    "List all tracking items"

    def take_action(self, parsed_args):
        data = [format(tracking)[1] for tracking
                in TrackingManager(self.app.client).list()]

        if data:
            return (format()[0], data)
        else:
            return format()
