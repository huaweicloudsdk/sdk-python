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

from openstack.cdn.exceptions import CDNException


class TestCDNException(testtools.TestCase):
    def test_unicode(self):
        sot = CDNException(message='msg', code='CDN.0001')
        expected = 'CDNException: msg(CDN.0001)'
        self.assertEqual(expected, str(sot))
