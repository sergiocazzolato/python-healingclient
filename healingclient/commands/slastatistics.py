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
from healingclient.api.slastatistics import SLAStatisticsManager

LOG = logging.getLogger(__name__)


def format(slastatistics=None):
    columns = (
        'Type',
        'Value',
    )

    if slastatistics:
        data = (
            slastatistics.type,
            slastatistics.value
        )
    else:
        data = []

    return columns, data


class Get(ShowCommand):
    "Show availability for a project/resource"

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)
        parser.add_argument(
            'type',
            choices=['availability', 'max_unavailable_period'],
            help='Type')
        parser.add_argument(
            '-project_id',
            help='Project ID')
        parser.add_argument(
            '-resource_id',
            help='Resource ID')
        parser.add_argument(
            '-from_date',
            help='From Date')
        parser.add_argument(
            '-to_date',
            help='To Date')
        return parser

    def take_action(self, parsed_args):
        slastatistics = SLAStatisticsManager(self.app.client).\
            get(parsed_args.type,
                parsed_args.project_id,
                parsed_args.from_date,
                parsed_args.to_date,
                parsed_args.resource_id)

        return format(slastatistics)
