# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
from arsenal.adapters.memory_datastore import MemoryDatastore
from arsenal.core.manager import Manager
from arsenal.drivers.ironic_synchronizer import IronicSynchronizer
from arsenal.interfaces.api import Api
from flask import Flask
from ironicclient import client

ironicclient = None
# TODO(wajdi): Move this in to config loader
if 'TRAVIS' not in os.environ:
    # TODO(wajdi): Make this a real config
    ironicclient = IronicSynchronizer(client.get_client(
        "1",
        os_username="admin",
        os_password="password",
        os_tenant_name="admin",
        os_auth_url="http://172.27.59.42:5000/v2.0/",
        os_region_name="RegionOne"
    ))


def wire_stuff(app):
    datastore = MemoryDatastore()
    # TODO(lindycoder): put a real thing in there if you got the TEST for it!
    Api(app, Manager(datastore, IronicSynchronizer(ironicclient)))

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

wire_stuff(app)
