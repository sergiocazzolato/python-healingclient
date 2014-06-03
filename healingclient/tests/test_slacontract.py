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

import json

from healingclient.tests import base
from healingclient.api.slacontract import SLAContract

# TODO: later we need additional tests verifying all the errors etc.

CONTRACTS = [
    {
        'tenant_id': "fake_tenant_0",
        'type': "fake_type_0",
        'value': "fake_value_0",
        'action': "fake_action_0"
    },
    {
        'id': 1,
        'tenant_id': "fake_tenant_1",
        'type': "fake_type_1",
        'value': "fake_value_1",
        'action': "fake_action_1"
    }
]

URL_TEMPLATE = '/sla/contract'
URL_TEMPLATE_NAME = '/sla/contract/%s'


class TestSLAContract(base.BaseClientTest):
    def test_create(self):
        mock = self.mock_http_post(content=CONTRACTS[0])

        wb = self.slacontract.create(CONTRACTS[0]['tenant_id'],
                                     CONTRACTS[0]['type'],
                                     CONTRACTS[0]['value'],
                                     CONTRACTS[0]['action'])

        self.assertIsNotNone(wb)
        self.assertEqual(SLAContract(self.slacontract, CONTRACTS[0]).
                         __dict__,
                         wb.__dict__)
        mock.assert_called_once_with(URL_TEMPLATE,
                                     json.dumps(CONTRACTS[0]))

    def test_update(self):
        mock = self.mock_http_put(content=CONTRACTS[1])

        wb = self.slacontract.update(CONTRACTS[1]['id'],
                                     CONTRACTS[1]['tenant_id'],
                                     CONTRACTS[1]['type'],
                                     CONTRACTS[1]['value'],
                                     CONTRACTS[1]['action'])

        self.assertIsNotNone(wb)
        self.assertEqual(SLAContract(self.slacontract, CONTRACTS[1]).
                         __dict__,
                         wb.__dict__)
        mock.assert_called_once_with(
            URL_TEMPLATE_NAME % CONTRACTS[1]['id'],
            json.dumps(CONTRACTS[1]))

    def test_list(self):
        mock = self.mock_http_get(content={'slacontracts': CONTRACTS})

        slacontracts = self.slacontract.list()

        self.assertEqual(2, len(slacontracts))
        wb = slacontracts[0]

        self.assertEqual(SLAContract(self.slacontract, CONTRACTS[0]).
                         __dict__,
                         wb.__dict__)
        mock.assert_called_once_with(URL_TEMPLATE)

    def test_get(self):
        mock = self.mock_http_get(content=CONTRACTS[1])

        wb = self.slacontract.get(CONTRACTS[1]['id'])

        self.assertIsNotNone(wb)
        self.assertEqual(SLAContract(self.slacontract, CONTRACTS[1]).
                         __dict__,
                         wb.__dict__)
        mock.assert_called_once_with(URL_TEMPLATE_NAME % CONTRACTS[1]['id'])

    def test_delete(self):
        mock = self.mock_http_delete(status_code=204)

        self.slacontract.delete(CONTRACTS[1]['id'])

        mock.assert_called_once_with(URL_TEMPLATE_NAME % CONTRACTS[1]['id'])
