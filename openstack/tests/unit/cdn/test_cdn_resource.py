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

from openstack.cdn import cdn_resource
from openstack.cdn.exceptions import CDNException
from openstack.exceptions import InvalidRequest
from openstack import resource2
from openstack import service_filter


class TestCDNResource(testtools.TestCase):
    def setUp(self):
        super(TestCDNResource, self).setUp()
        self.base_path = '/base_path'
        self.session = mock.Mock()

        class TestService(service_filter.ServiceFilter):
            valid_versions = [service_filter.ValidVersion('v2')]

            def __init__(self, version=None):
                super(TestService, self).__init__(service_type="service",
                                                  version=version)

        class Test(cdn_resource.Resource):
            base_path = self.base_path
            resource_key = 'resource'
            resources_key = 'resources'
            service = TestService()
            allow_list = True

        self.sot = Test()
        self.test_class = Test

    def test_basic(self):
        sot = cdn_resource.Resource()
        self.assertEqual('total', sot.total_path)
        self.assertEqual('page_number', sot.query_page_number_key)
        self.assertEqual('page_size', sot.query_page_size_key)

    def test_list(self):
        pass

    def test_get_next_pagination(self):
        resp = {'total': 0, 'domains': []}
        query_params = {'page_size': 10, 'page_number': 1}

        sot = cdn_resource.Resource()
        more, next_page_number = sot.get_next_pagination(resp, query_params)
        self.assertFalse(more)
        self.assertEqual(1, next_page_number)

    def test_get_next_pagination_more(self):
        resp = {'total': 100, 'domains': []}
        query_params = {'page_size': 10, 'page_number': 1}

        sot = cdn_resource.Resource()
        more, next_page_number = sot.get_next_pagination(resp, query_params)
        self.assertTrue(more)
        self.assertEqual(2, next_page_number)

    def test__translate_response_no_body(self):
        class Test(cdn_resource.Resource):
            attr = resource2.Header("attr")

        response = mock.Mock()
        response.headers = dict()

        sot = Test()
        sot._filter_component = mock.Mock(return_value={"attr": "value"})

        sot._translate_response(response, has_body=False)

        self.assertEqual(dict(), sot._header.dirty)
        self.assertEqual("value", sot.attr)

    def test__translate_response_with_body_no_resource_key(self):
        class Test(cdn_resource.Resource):
            attr = resource2.Body("attr")

        body = {"attr": "value"}
        response = mock.Mock()
        response.headers = dict()
        response.json.return_value = body

        sot = Test()
        sot._filter_component = mock.Mock(side_effect=[body, dict()])

        sot._translate_response(response, has_body=True)

        self.assertEqual("value", sot.attr)
        self.assertEqual(dict(), sot._body.dirty)
        self.assertEqual(dict(), sot._header.dirty)

    def test__translate_response_with_body_with_resource_key(self):
        key = "key"

        class Test(cdn_resource.Resource):
            resource_key = key
            attr = resource2.Body("attr")

        body = {"attr": "value"}
        response = mock.Mock()
        response.headers = dict()
        response.json.return_value = {key: body}

        sot = Test()
        sot._filter_component = mock.Mock(side_effect=[body, dict()])

        sot._translate_response(response, has_body=True)

        self.assertEqual("value", sot.attr)
        self.assertEqual(dict(), sot._body.dirty)
        self.assertEqual(dict(), sot._header.dirty)

    def test__translate_response_with_error(self):
        key = "key"

        class Test(cdn_resource.Resource):
            resource_key = key
            attr = resource2.Body("attr")

        body = {"error": {"error_msg": "msg", "error_code": "CDN.0000"}}
        response = mock.Mock()
        response.headers = dict()
        response.json.return_value = body

        sot = Test()

        self.assertRaises(CDNException, sot._translate_response,
                          response, has_body=True)

    def test_list_without_pagination_params(self):
        def wrapper(sess):
            return list(self.sot.list(sess))

        self.assertRaises(InvalidRequest, wrapper, self.session)

    # NOTE: As list returns a generator, testing it requires consuming
    # the generator. Wrap calls to self.sot.list in a `list`
    # and then test the results as a list of responses.
    def test_list_empty_response(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {'total': 0, 'resources': []}
        query_params = {'page_size': 10, 'page_number': 1}

        self.session.get.return_value = mock_response

        result = list(self.sot.list(self.session, **query_params))

        self.session.get.assert_called_once_with(
            self.base_path,
            endpoint_filter=self.sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=query_params)

        self.assertEqual([], result)

    def test_list_one_page_response_paginated(self):
        id_value = 1
        mock_response = mock.Mock()
        mock_response.json.return_value = {'total': 1,
                                           'resources': [{"id": id_value}]}
        query_params = {'page_size': 10, 'page_number': 1}

        self.session.get.return_value = mock_response

        # Ensure that we break out of the loop on a paginated call
        # that still only results in one page of data.
        results = list(self.sot.list(self.session, paginated=True,
                                     **query_params))

        self.assertEqual(1, len(results))

        # Look at the `params` argument to each of the get calls that
        # were made.
        self.session.get.call_args_list[0][1]["params"] = query_params
        self.assertEqual(id_value, results[0].id)
        self.assertIsInstance(results[0], self.test_class)

    def test_list_one_page_response_not_paginated(self):
        id_value = 1
        mock_response = mock.Mock()
        mock_response.json.return_value = {'total': 1,
                                           'resources': [{"id": id_value}]}
        query_params = {'page_size': 10, 'page_number': 1}

        self.session.get.return_value = mock_response

        results = list(self.sot.list(self.session, paginated=False,
                                     **query_params))

        self.session.get.assert_called_once_with(
            self.base_path,
            endpoint_filter=self.sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=query_params)
        self.assertEqual(1, len(results))
        self.assertEqual(id_value, results[0].id)
        self.assertIsInstance(results[0], self.test_class)

    def test_list_multi_page_response_not_paginated(self):
        ids = [1, 2]
        mock_response = mock.Mock()
        mock_response.json.return_value = {'total': 2,
                                           'resources': [{"id": ids[0]}]}
        query_params = {'page_size': 1, 'page_number': 1}

        self.session.get.return_value = mock_response

        results = list(self.sot.list(self.session, paginated=False,
                                     **query_params))

        self.session.get.assert_called_once_with(
            self.base_path,
            endpoint_filter=self.sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=query_params)
        self.assertEqual(1, len(results))
        self.assertEqual(ids[0], results[0].id)
        self.assertIsInstance(results[0], self.test_class)

    def test_list_multi_page_response_paginated(self):
        # This tests our ability to stop making calls once
        # we've received all of the data. However, this tests
        # the case that we always receive full pages of data
        # and then the signal that there is no more data - an empty list.
        # In this case, we need to make one extra request beyond
        # the end of data to ensure we've received it all.
        ids = [1, 2]
        resp1 = mock.Mock()
        resp1.json.return_value = {'total': 2,
                                   'resources': [{'id': ids[0]}]}
        resp2 = mock.Mock()
        resp2.json.return_value = {'total': 2,
                                   'resources': [{'id': ids[1]}]}
        query_params = {'page_size': 1, 'page_number': 1}

        self.session.get.side_effect = [resp1, resp2]

        results = self.sot.list(self.session, paginated=True, **query_params)

        result0 = next(results)
        self.assertEqual(result0.id, ids[0])
        self.session.get.assert_called_with(
            self.base_path,
            endpoint_filter=self.sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=query_params)

        result1 = next(results)
        self.assertEqual(result1.id, ids[1])
        query_params['page_number'] += 1
        self.session.get.assert_called_with(
            self.base_path,
            endpoint_filter=self.sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=query_params)

        self.assertRaises(StopIteration, next, results)


class TestQueryParameters(testtools.TestCase):
    def test_basic(self):
        sot = cdn_resource.QueryParameters()

        self.assertDictEqual({'page_size': 'page_size',
                              'page_number': 'page_number'}, sot._mapping)


class TestStatisticParameters(testtools.TestCase):
    def test_basic(self):
        sot = cdn_resource.StatisticParameters()

        self.assertDictEqual({'start_time': 'start_time',
                              'end_time': 'end_time',
                              'domain_name': 'domain_name'}, sot._mapping)
