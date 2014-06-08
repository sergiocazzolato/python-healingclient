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
from healingclient.api.actions import ActionManager

LOG = logging.getLogger(__name__)


def format(action=None):
    columns = (
        'ID',
        'Name',
        'Created_At',
        'Status',
        'Output',
        'Target_Resource',
        'Track ID')
        
    if action:
        data = (
            action.id,
            action.name,
            action.created_at,
            action.status,
            action.output,
            action.target_id,
            action.request_id
            )
    else:
        data = []

    return columns, data


class List(ListCommand):
    "List all actions."""
    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument(
            '-track_id',
            help='Request ID / Track ID')
        parser.add_argument(
            '-name',
            help='By name ( override track_id)')
            
        return parser


    def take_action(self, parsed_args):
        resource_id = parsed_args.track_id
        name = parsed_args.name
        
        data = [format(action)[1] for action
                in ActionManager(self.app.client).list(resource_id, name)]

        if data:
            return (format()[0], data)
        else:
            return format()


