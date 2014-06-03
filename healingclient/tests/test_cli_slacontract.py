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

import mock

from healingclient.tests import base

from healingclient.commands import slacontract
from healingclient.api.slacontract import SLAContract

SLA_CONTRACT = SLAContract(mock, {
    'id': 0,
    'tenant_id': "fake_tenant_0",
    'type': "fake_type_0",
    'value': "fake_value_0",
    'action': "fake_action_0"
})


class TestCLISLAContract(base.BaseCommandTest):
    @mock.patch('healingclient.api.slacontract.SLAContractManager.create')
    def test_create(self, mock):
        mock.return_value = SLA_CONTRACT

        result = self.call(slacontract.Create, app_args=['tenant_id',
                                                         'type', 'value',
                                                         'action'])
        self.assertEqual((0, 'fake_tenant_0', 'fake_type_0', 'fake_value_0',
                          'fake_action_0'), result[1])

    @mock.patch('healingclient.api.slacontract.SLAContractManager.update')
    def test_update(self, mock):
        mock.return_value = SLA_CONTRACT

        result = self.call(slacontract.Update, app_args=['id', 'tenant_id',
                                                         'type', 'value',
                                                         'action'])

        self.assertEqual((0, 'fake_tenant_0', 'fake_type_0', 'fake_value_0',
                          'fake_action_0'), result[1])

    @mock.patch('healingclient.api.slacontract.SLAContractManager.list')
    def test_list(self, mock):
        mock.return_value = (SLA_CONTRACT,)

        result = self.call(slacontract.List)

        self.assertEqual([(0, 'fake_tenant_0', 'fake_type_0', 'fake_value_0',
                          'fake_action_0')], result[1])

    @mock.patch('healingclient.api.slacontract.SLAContractManager.get')
    def test_get(self, mock):
        mock.return_value = SLA_CONTRACT

        result = self.call(slacontract.Get, app_args=['id'])

        self.assertEqual((0, 'fake_tenant_0', 'fake_type_0', 'fake_value_0',
                          'fake_action_0'), result[1])

    @mock.patch('healingclient.api.slacontract.SLAContractManager.delete')
    def test_delete(self, mock):
        self.assertIsNone(self.call(slacontract.Delete, app_args=['id']))
