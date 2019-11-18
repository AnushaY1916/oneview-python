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

from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# To run this example, you may set a WWN to add a volume using the WWN of the volume (optional)
unmanaged_volume_wwn = ''

oneview_client = OneViewClient(config)

# Defines the storage system and the storage pool which are provided to create the volumes
storage_system = oneview_client.storage_systems.get_all()[0]
storage_pools = oneview_client.storage_pools.get_all()
storage_pool_available = False
for sp in storage_pools:
    if sp['storageSystemUri'] == storage_system['uri']:
        storage_pool_available = True
        storage_pool = sp
if not storage_pool_available:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

# Create a volume with a Storage Pool
print("\nCreate a volume with a specified Storage Pool and Snapshot Pool")

options = {
    "properties": {
        "storagePool": storage_pool['uri'],
        "size": 1024 * 1024 * 1024,  # 1GB
        "isShareable": False,
        "snapshotPool": storage_pool['uri'],
        "provisioningType": "Thin",
        "name": "ONEVIEW_SDK_TEST_VOLUME_TYPE_1"
    },
    "templateUri": "/rest/storage-volume-templates/6da3016e-7ced-4e0b-8dac-a8b200a66e4f",
    "isPermanent": False
}

new_volume = oneview_client.volumes.create(options)
pprint(new_volume)

# Add a volume for management by the appliance using the WWN of the volume
if unmanaged_volume_wwn:
    print("\nAdd a volume for management by the appliance using the WWN of the volume")

    options_with_wwn = {
        "type": "AddStorageVolumeV2",
        "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_4',
        "description": 'Test volume added for management: Storage System + Storage Pool + WWN',
        "storageSystemUri": storage_system['uri'],
        "wwn": unmanaged_volume_wwn,
        "provisioningParameters": {
            "shareable": False
        }
    }
    volume_added_with_wwn = oneview_client.volumes.create(options_with_wwn)
    pprint(volume_added_with_wwn)

# Get all managed volumes
print("\nGet a list of all managed volumes")
volumes = oneview_client.volumes.get_all()
for volume in volumes:
    print("Name: {name}".format(**volume))

# Find a volume by name
volume = oneview_client.volumes.get_by('name', new_volume['name'])[0]
print("\nFound a volume by name: '{name}'.\n  uri = '{uri}'".format(**volume))

# Update the name of the volume recently found to 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume['name'] = 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume = oneview_client.volumes.update(volume)
print("\nVolume updated successfully.\n  uri = '{uri}'\n  with attribute 'name' = {name}".format(**volume))

# Find a volume by URI
volume_uri = new_volume['uri']
volume = oneview_client.volumes.get(volume_uri)
print("\nFind a volume by URI")
pprint(volume)

# Create a snapshot
print("\nCreate a snapshot")

snapshot_options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot"
}
volume_with_snapshot_pool = oneview_client.volumes.create_snapshot(new_volume['uri'], snapshot_options)
print("Created a snapshot for the volume '{name}'".format(**new_volume))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
created_snapshot = oneview_client.volumes.get_snapshot_by(new_volume['uri'], 'name', 'Test Snapshot')[0]
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**created_snapshot))

snapshot_uri = created_snapshot['uri']

# Get recently created snapshot resource by uri
print("\nGet a snapshot")
try:
    snapshot = oneview_client.volumes.get_snapshot(snapshot_uri, volume_uri)
    pprint(snapshot)
except HPOneViewException as e:
    print(e.msg)

# Get a paginated list of snapshot resources sorting by name ascending
print("\nGet a list of the first 10 snapshots")
snapshots = oneview_client.volumes.get_snapshots(new_volume['uri'], 0, 10, sort='name:ascending')
for snapshot in snapshots:
    print('  {name}'.format(**snapshot))

# Delete the recently created snapshot resource
print("\nDelete the recently created snapshot")
returned = oneview_client.volumes.delete_snapshot(created_snapshot)
print("Snapshot deleted successfully")

# Get the list of all extra managed storage volume paths from the appliance
extra_volumes = oneview_client.volumes.get_extra_managed_storage_volume_paths()
print("\nGet the list of all extra managed storage volume paths from the appliance")
pprint(extra_volumes)

# Remove extra presentations from the specified volume on the storage system
print("\nRemove extra presentations from the specified volume on the storage system")
oneview_client.volumes.repair(volume['uri'])
print("  Done.")

# Get all the attachable volumes which are managed by the appliance
print("\nGet all the attachable volumes which are managed by the appliance")
attachable_volumes = oneview_client.volumes.get_attachable_volumes()
pprint(attachable_volumes)

print("\nGet the attachable volumes which are managed by the appliance with scopes and connections")
scope_uris = ['/rest/scopes/e4a23533-9a72-4375-8cd3-a523016df852', '/rest/scopes/7799327d-6d79-4eb2-b969-a523016df869']

connections = [{'networkUri': '/rest/fc-networks/90bd0f63-3aab-49e2-a45f-a52500b46616',
                'proxyName': '20:19:50:EB:1A:0F:0E:B6', 'initiatorName': '10:00:62:01:F8:70:00:0E'},
               {'networkUri': '/rest/fc-networks/8acd0f62-1aab-49e2-a45a-d22500b4acdb',
                'proxyName': '20:18:40:EB:1A:0F:0E:C7', 'initiatorName': '10:00:72:01:F8:70:00:0F'}]
attachable_volumes = oneview_client.volumes.get_attachable_volumes(scope_uris=scope_uris, connections=connections)
pprint(attachable_volumes)

print("\nDelete the recently created volumes")
if oneview_client.volumes.delete(new_volume):
    print("The volume, that was previously created with a Storage Pool, was deleted from OneView and storage system")
if unmanaged_volume_wwn and oneview_client.volumes.delete(volume_added_with_wwn, export_only=True):
    print("The volume, that was previously added using the WWN of the volume, was deleted from OneView")
