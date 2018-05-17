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

import mock
import testtools

from openstack.cdn.v1 import statistic


class TestStatistic(testtools.TestCase):
    def setUp(self):
        super(TestStatistic, self).setUp()

        class Test(statistic.Statistic):
            base_path = '/cdn/statistics/test'
            resource_key = 'resource'

        self.sot = Test()

    def _verify(self, test_method, mock_method,
                mock_json=None,
                method_args=[], method_kwargs={},
                expected_args=[], expected_kwargs={}):
        resp = mock.Mock()
        resp.json.return_value = mock_json
        resp.headers = {}
        sess = mock.Mock()
        mocked = getattr(sess, mock_method)
        mocked.return_value = resp

        method_args = [sess] + method_args
        actual_result = test_method(*method_args, **method_kwargs)
        mocked.assert_called_once_with(*expected_args, **expected_kwargs)
        return actual_result

    def test_query(self):
        url = '/cdn/statistics/test'
        body = {
            "resource": {
                "start_time": 1498838400000,
                "end_time": 1502380500000,
                "value": 835038583
            }
        }
        kwargs = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain'
        }
        expected_kwargs = {
            'endpoint_filter': self.sot.service,
            'endpoint_override': None,
            'params': kwargs
        }
        self._verify(self.sot.query, 'get',
                     mock_json=body,
                     method_kwargs=kwargs,
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)


class TestStatisticDetail(testtools.TestCase):
    def setUp(self):
        super(TestStatisticDetail, self).setUp()

        class Test(statistic.StatisticDetail):
            base_path = '/cdn/statistics/test-detail'
            resource_key = 'resource'

        self.sot = Test()

    def _verify(self, test_method, mock_method,
                mock_json=None,
                method_args=[], method_kwargs={},
                expected_args=[], expected_kwargs={}):
        resp = mock.Mock()
        resp.json.return_value = mock_json
        resp.headers = {}
        sess = mock.Mock()
        mocked = getattr(sess, mock_method)
        mocked.return_value = resp

        method_args = [sess] + method_args
        actual_result = test_method(*method_args, **method_kwargs)
        mocked.assert_called_once_with(*expected_args, **expected_kwargs)
        return actual_result

    def test_query(self):
        url = '/cdn/statistics/test-detail'
        body = {
            "resource": {
                "start_time": 1498838400000,
                "end_time": 1502380500000,
                "interval": 300,
                "values": [1, 2, 3]
            }
        }
        kwargs = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain'
        }
        expected_kwargs = {
            'endpoint_filter': self.sot.service,
            'endpoint_override': None,
            'params': kwargs
        }
        self._verify(self.sot.query, 'get',
                     mock_json=body,
                     method_kwargs=kwargs,
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)


class TestNetworkTraffic(testtools.TestCase):
    def test_basic(self):
        sot = statistic.NetworkTraffic()
        self.assertEqual('/cdn/statistics/flux', sot.base_path)
        self.assertEqual('flux', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1498838400000,
            "end_time": 1502380500000,
            "value": 835038583
        }
        sot = statistic.NetworkTraffic(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['value'], sot.value)


class TestNetworkTrafficDetail(testtools.TestCase):
    def test_basic(self):
        sot = statistic.NetworkTrafficDetail()
        self.assertEqual('/cdn/statistics/flux-detail', sot.base_path)
        self.assertEqual('flux_detail', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name',
                              'interval': 'interval'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1498838400000,
            "end_time": 1502380500000,
            "interval": 300,
            "values": [835038583, 835038584]
        }
        sot = statistic.NetworkTrafficDetail(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['interval'], sot.interval)
        self.assertItemsEqual(EXAMPLE['values'], sot.values)


class TestBandwidthPeak(testtools.TestCase):
    def test_basic(self):
        sot = statistic.BandwidthPeak()
        self.assertEqual('/cdn/statistics/bandwidth', sot.base_path)
        self.assertEqual('bandwidth', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1498838400000,
            "end_time": 1502380500000,
            "peak_time": 1502380400000,
            "value": 835038583
        }
        sot = statistic.BandwidthPeak(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['peak_time'], sot.peaked_at)
        self.assertEqual(EXAMPLE['value'], sot.value)


class TestBandWidthDetail(testtools.TestCase):
    def test_basic(self):
        sot = statistic.BandwidthDetail()
        self.assertEqual('/cdn/statistics/bandwidth-detail', sot.base_path)
        self.assertEqual('bandwidth_detail', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name',
                              'interval': 'interval'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1498838400000,
            "end_time": 1502380500000,
            "interval": 300,
            "values": [835038583, 835038584]
        }
        sot = statistic.BandwidthDetail(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['interval'], sot.interval)
        self.assertItemsEqual(EXAMPLE['values'], sot.values)


class TestConsumptionSummary(testtools.TestCase):
    def test_basic(self):
        sot = statistic.ConsumptionSummary()
        self.assertEqual('/cdn/statistics/domain-summary', sot.base_path)
        self.assertEqual('domain_summary', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name',
                              'stat_type': 'stat_type',
                              'service_area': 'service_area'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1513094400000,
            "end_time": 1513180799346,
            "value": 835038583,
            "stat_type": "flux_hit_rate",
            "service_area": "mainland_china"
        }
        sot = statistic.ConsumptionSummary(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['value'], sot.value)
        self.assertEqual(EXAMPLE['stat_type'], sot.stat_type)
        self.assertEqual(EXAMPLE['service_area'], sot.service_area)


class TestConsumptionSummaryDetail(testtools.TestCase):
    def test_basic(self):
        sot = statistic.ConsumptionSummaryDetail()
        self.assertEqual('/cdn/statistics/domain-summary-detail',
                         sot.base_path)
        self.assertEqual('domain_summary_detail', sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name',
                              'interval': 'interval',
                              'stat_type': 'stat_type',
                              'service_area': 'service_area'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        EXAMPLE = {
            "start_time": 1498838400000,
            "end_time": 1502380500000,
            "interval": 300,
            "stat_type": "bs_flux",
            "values": [835038583, 835038584],
            "service_area": "outside_mainland_china"
        }
        sot = statistic.ConsumptionSummaryDetail(**EXAMPLE)
        self.assertEqual(EXAMPLE['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['interval'], sot.interval)
        self.assertEqual(EXAMPLE['stat_type'], sot.stat_type)
        self.assertEqual(EXAMPLE['service_area'], sot.service_area)
        self.assertItemsEqual(EXAMPLE['values'], sot.values)
