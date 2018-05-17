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

import testtools

from openstack.cdn.v1 import log

IDENTIFIER = ''
EXAMPLE = {
    "domain_name": "www.xxxx.com",
    "start_time": "1498838400000",
    "end_time": "1502380500000",
    "name": "www.xxxx.com-2017080315",
    "link": "www.xxxx.web",
    "size": 4096
}


class TestLog(testtools.TestCase):
    def test_basic(self):
        sot = log.Log()
        self.assertEqual('log', sot.resource_key)
        self.assertEqual('logs', sot.resources_key)
        self.assertEqual('/cdn/logs', sot.base_path)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({'page_size': 'page_size',
                              'page_number': 'page_number',
                              'query_date': 'query_date',
                              'domain_name': 'domain_name'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = log.Log(**EXAMPLE)
        self.assertEqual(EXAMPLE['domain_name'], sot.domain_name)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['link'], sot.link)
        self.assertEqual(EXAMPLE['size'], sot.size)
