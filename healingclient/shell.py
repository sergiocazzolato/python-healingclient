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

"""
Command-line interface to the Healing APIs
"""

import sys

from healingclient.openstack.common.cliutils import env
from healingclient.openstack.common import log as logging

from healingclient.api.client import Client

import healingclient.commands.slacontract


from cliff.app import App
from cliff.help import HelpAction
from cliff.commandmanager import CommandManager

import argparse

LOG = logging.getLogger(__name__)


class HealingShell(App):

    def __init__(self):
        super(HealingShell, self).__init__(
            description=__doc__.strip(),
            version='0.1',
            command_manager=CommandManager('healing.cli'),
        )

        self.commands = {
            'sla-contract-list': healingclient.commands.slacontract.List,
            'sla-contract-get': healingclient.commands.slacontract.Get,
            'sla-contract-create': healingclient.commands.slacontract.Create,
            'sla-contract-update': healingclient.commands.slacontract.Update,
            'sla-contract-delete': healingclient.commands.slacontract.Delete,
        }

        for k, v in self.commands.items():
            self.command_manager.add_command(k, v)

    def build_option_parser(self, description, version,
                            argparse_kwargs=None):
        """Return an argparse option parser for this application.

        Subclasses may override this method to extend
        the parser with more global options.

        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        :param argparse_kwargs: extra keyword argument passed to the
                                ArgumentParser constructor
        :paramtype extra_kwargs: dict
        """
        argparse_kwargs = argparse_kwargs or {}
        parser = argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {0}'.format(version),
            help='Show program\'s version number and exit.'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output. Can be repeated.',
        )
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        parser.add_argument(
            '-q', '--quiet',
            action='store_const',
            dest='verbose_level',
            const=0,
            help='Suppress output except warnings and errors.',
        )
        parser.add_argument(
            '-h', '--help',
            action=HelpAction,
            nargs=0,
            default=self,  # tricky
            help="Show this help message and exit.",
        )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='Show tracebacks on errors.',
        )
        parser.add_argument(
            '--os-healing_url',
            action='store',
            dest='healing_url',
            default=env('OS_HEALING_URL', default='http://localhost:9999/v1'),
            help='Healing API host (Env: OS_HEALING_URL)'
        )
        parser.add_argument(
            '--os-username',
            action='store',
            dest='username',
            default=env('OS_USERNAME', default='admin'),
            help='Authentication username (Env: OS_USERNAME)'
        )
        parser.add_argument(
            '--os-password',
            action='store',
            dest='password',
            default=env('OS_PASSWORD', default='openstack'),
            help='Authentication password (Env: OS_PASSWORD)'
        )
        parser.add_argument(
            '--os-tenant-id',
            action='store',
            dest='tenant_id',
            default=env('OS_TENANT_ID'),
            help='Authentication tenant identifier (Env: OS_TENANT_ID)'
        )
        parser.add_argument(
            '--os-tenant-name',
            action='store',
            dest='tenant_name',
            default=env('OS_TENANT_NAME', 'Default'),
            help='Authentication tenant name (Env: OS_TENANT_NAME)'
        )
        parser.add_argument(
            '--os-auth-token',
            action='store',
            dest='token',
            default=env('OS_AUTH_TOKEN'),
            help='Authentication token (Env: OS_AUTH_TOKEN)'
        )
        parser.add_argument(
            '--os-auth-url',
            action='store',
            dest='auth_url',
            default=env('OS_AUTH_URL'),
            help='Authentication URL (Env: OS_AUTH_URL)'
        )
        return parser

    def initialize_app(self, argv):
        self.client = Client(healing_url=self.options.healing_url,
                             username=self.options.username,
                             api_key=self.options.password,
                             project_name=self.options.tenant_name,
                             auth_url=self.options.auth_url,
                             project_id=self.options.tenant_id,
                             endpoint_type='publicURL',
                             service_type='healing',
                             auth_token=self.options.token)


def main(argv=sys.argv[1:]):
    return HealingShell().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
