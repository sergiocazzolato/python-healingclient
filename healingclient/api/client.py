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

from keystoneclient.v3 import client as keystone_client

from healingclient.api import httpclient
from healingclient.api import slacontract


class Client(object):
    def __init__(self, healing_url=None, username=None, api_key=None,
                 project_name=None, auth_url=None, project_id=None,
                 endpoint_type='publicURL', service_type='healing',
                 auth_token=None, user_id=None):

        if healing_url and not isinstance(healing_url, six.string_types):
            raise RuntimeError('Healing url should be string')

        if auth_url:
            (healing_url, auth_token, project_id, user_id) = \
                self.authenticate(healing_url, username, api_key,
                                  project_name, auth_url, project_id,
                                  endpoint_type, service_type, auth_token,
                                  user_id)

        if not healing_url:
            healing_url = "http://localhost:9999/v1"

        self.http_client = httpclient.HTTPClient(healing_url,
                                                 auth_token,
                                                 project_id,
                                                 user_id)
        # Create all resource managers.
        self.slacontract = slacontract.SLAContractManager(self)

    def authenticate(self, healing_url=None, username=None, api_key=None,
                     project_name=None, auth_url=None, project_id=None,
                     endpoint_type='publicURL', service_type='healing',
                     auth_token=None, user_id=None):

        if (not (project_name or project_id) or
            not (isinstance(project_name, six.string_types) or
                 isinstance(project_id, six.string_types))):
            raise RuntimeError('Either project name or project id should'
                               ' be non-empty string')
        if project_name and project_id:
            raise RuntimeError('Only project name or '
                               'project id should be set')

        if (not (username or user_id) or
            not (isinstance(username, six.string_types) or
                 isinstance(user_id, six.string_types))):
            raise RuntimeError('Either user name or user id should'
                               ' be non-empty string')
        if username and user_id:
            raise RuntimeError('Only user name or user id'
                               ' should be set')

        if "v2.0" in auth_url:
            raise RuntimeError('Healing supports only v3  '
                               'keystone API. Please see help and '
                               'configure the correct auth url.')

        keystone = keystone_client.Client(username=username,
                                          user_id=user_id,
                                          password=api_key,
                                          token=auth_token,
                                          project_id=project_id,
                                          project_name=project_name,
                                          auth_url=auth_url)

        keystone.authenticate()
        token = keystone.auth_token
        user_id = keystone.user_id
        project_id = keystone.project_id

        if not healing_url:
            catalog = keystone.service_catalog.get_endpoints(
                service_type=service_type,
                endpoint_type=endpoint_type
            )
            if service_type in catalog:
                service = catalog.get(service_type)
                healing_url = service[0].get('url') if service else None

        return healing_url, token, project_id, user_id
