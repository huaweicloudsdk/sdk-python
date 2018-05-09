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

from openstack.cdn import format


class TestBoolIntFormatter(testtools.TestCase):

    def test_deserialize(self):
        self.assertTrue(format.BoolInt.deserialize(1))
        self.assertFalse(format.BoolInt.deserialize(0))
        self.assertFalse(format.BoolInt.deserialize(None))
        self.assertTrue(format.BoolInt.deserialize(True))
        self.assertRaises(ValueError, format.BoolInt.deserialize, '')
        self.assertRaises(ValueError, format.BoolInt.deserialize, 2)

    def test_serialize(self):
        self.assertEqual(1, format.BoolInt.serialize(True))
        self.assertEqual(0, format.BoolInt.serialize(False))
        self.assertEqual(1, format.BoolInt.serialize(1))
        self.assertRaises(ValueError, format.BoolInt.serialize, None)
        self.assertRaises(ValueError, format.BoolInt.serialize, 2)
