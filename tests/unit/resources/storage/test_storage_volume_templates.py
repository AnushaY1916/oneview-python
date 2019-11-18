# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.resource import ResourceClient


class StorageVolumeTemplatesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_volume_templates = StorageVolumeTemplates(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_volume_templates.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_volume_templates.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        storage_volume_templates_id = "EE9326ED-4595-4828-B411-FE3BD6BA7E9D"
        self._storage_volume_templates.get(storage_volume_templates_id)
        mock_get.assert_called_once_with(storage_volume_templates_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        storage_volume_templates_uri = "/rest/storage-volume-templates/EE9326ED-4595-4828-B411-FE3BD6BA7E9D"
        self._storage_volume_templates.get(storage_volume_templates_uri)
        mock_get.assert_called_once_with(storage_volume_templates_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        storage_volume_template = {
            "name": "FusionTemplateExample",
            "provisioning": {
                "shareable": True,
                "provisionType": "Thin",
                "capacity": "235834383322",
                "storagePoolUri": "/rest/storage-pools/{id}"
            },
            "stateReason": "None",
            "storageSystemUri": "/rest/storage-systems/{id}",
            "snapshotPoolUri": "/rest/storage-pools/{id}"
        }
        self._storage_volume_templates.create(storage_volume_template, 70)
        mock_create.assert_called_once_with(
            storage_volume_template, timeout=70, custom_headers={'Accept-Language': 'en_US'},
            default_values=self._storage_volume_templates.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_volume_templates.delete(id, force=True, timeout=50)
        mock_delete.assert_called_once_with(id, force=True, timeout=50, custom_headers={
            'Accept-Language': 'en_US', 'If-Match': '*'})

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_volume_templates.delete(id)
        mock_delete.assert_called_once_with(id, force=False, timeout=-1, custom_headers={
            'Accept-Language': 'en_US', 'If-Match': '*'})

    @mock.patch.object(ResourceClient, 'get')
    def test_get_connectable_volume_templates_called_once(self, mock_get):
        uri = '/rest/storage-volume-templates/connectable-volume-templates?start=0&count=-1'
        self._storage_volume_templates.get_connectable_volume_templates()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_reachable_volume_templates_called_once(self, mock_get):
        uri = '/rest/storage-volume-templates/reachable-volume-templates?networks=/rest/fake&privateAllowedOnly=False&start=0&count=-1'
        self._storage_volume_templates.get_reachable_volume_templates(networks='/rest/fake')
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_compatible_systems_called_once(self, mock_get):
        uri = '/rest/storage-volume-templates/fake/compatible-systems'
        self._storage_volume_templates.get_compatible_systems('/rest/storage-volume-templates/fake')
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        storage_volume_template = {
            "type": "StorageVolumeTemplateV3",
            "provisioning": {
                "shareable": True,
                "provisionType": "Thin",
                "capacity": "235834383322",
                "storagePoolUri": "/rest/storage-pools/{id}"
            },
            "name": "FusionTemplateExample",
        }
        self._storage_volume_templates.update(storage_volume_template, 70)
        mock_update.assert_called_once_with(
            storage_volume_template, timeout=70, custom_headers={'Accept-Language': 'en_US'},
            default_values=self._storage_volume_templates.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_volume_templates.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")
