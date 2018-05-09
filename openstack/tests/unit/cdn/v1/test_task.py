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

from openstack.cdn.v1 import task

IDENTIFIER = '8a29d3f05d0cbeee015d0cc1333c0007'
EXAMPLE = {
    "id": "8a29d3f05d0cbeee015d0cc1333c0007",
    "task_type": "preheating",
    "status": "task_done",
    "total": 4,
    "processing": 2,
    "succeed": 0,
    "failed": 4,
    "urls": [
        {
            "url": "https://www.xxx.cn/test/dir.png",
            "id": "8a29d3f05d0cbeee015d0cc133440009",
            "status": "failed",
            "create_time": 1499157542180,
            "task_id": "8a29d3f05d0cbeee015d0cc1333c0007"
        },
        {
            "url": "http://www.xxx.com/test15.jpg",
            "id": "8a29d3f05d0cbeee015d0cc133430008",
            "status": "failed",
            "create_time": 1499157542180,
            "task_id": "8a29d3f05d0cbeee015d0cc1333c0007"
        }
    ],
    "create_time": 1499157542180
}


class TestTask(testtools.TestCase):
    def test_basic(self):
        sot = task.Task()
        self.assertEqual('task', sot.resource_key)
        self.assertEqual('tasks', sot.resources_key)
        self.assertEqual('/cdn/historytasks', sot.base_path)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({'page_size': 'page_size',
                              'page_number': 'page_number',
                              'status': 'status',
                              'start_date': 'start_date',
                              'end_date': 'end_date',
                              'order_field': 'order_field',
                              'order_type': 'order_type',
                              'user_domain_id': 'user_domain_id'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = task.Task(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['task_type'], sot.task_type)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['total'], sot.total)
        self.assertEqual(EXAMPLE['processing'], sot.processing)
        self.assertEqual(EXAMPLE['succeed'], sot.succeeded)
        self.assertEqual(EXAMPLE['failed'], sot.failed)
        self.assertItemsEqual(EXAMPLE['urls'], sot.urls)
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)

    def test_list_order_by_prcesss(self):
        resp = mock.Mock()
        resp.json.return_value = {'total': 0, 'tasks': []}
        sess = mock.Mock()
        sess.get.return_value = resp

        sot = task.Task()
        params = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'processing',
            'order_type': 'asc'
        }
        mapped = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'process',
            'order_type': 'asc'
        }
        result = list(sot.list(sess, **params))

        sess.get.assert_called_once_with(
            sot.base_path,
            endpoint_filter=sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=mapped
        )
        self.assertEqual([], result)

    def test_list_order_by_created_at(self):
        resp = mock.Mock()
        resp.json.return_value = {'total': 0, 'tasks': []}
        sess = mock.Mock()
        sess.get.return_value = resp

        sot = task.Task()
        params = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'created_at',
            'order_type': 'asc'
        }
        mapped = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'create_time',
            'order_type': 'asc'
        }
        result = list(sot.list(sess, **params))

        sess.get.assert_called_once_with(
            sot.base_path,
            endpoint_filter=sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=mapped
        )
        self.assertEqual([], result)

    def test_list_order_by_status(self):
        resp = mock.Mock()
        resp.json.return_value = {'total': 0, 'tasks': []}
        sess = mock.Mock()
        sess.get.return_value = resp

        sot = task.Task()
        params = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'status',
            'order_type': 'asc'
        }
        mapped = {
            'page_size': 100,
            'page_number': 1,
            'order_field': 'status',
            'order_type': 'asc'
        }
        result = list(sot.list(sess, **params))

        sess.get.assert_called_once_with(
            sot.base_path,
            endpoint_filter=sot.service,
            endpoint_override=None,
            headers={"Accept": "application/json"},
            params=mapped
        )
        self.assertEqual([], result)

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

    def test_get(self):
        sot = task.Task(id=IDENTIFIER)
        url = 'cdn/historytasks/%s/detail' % IDENTIFIER
        expected_args = [url]
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }

        self._verify(sot.get, 'get',
                     mock_json={'id': IDENTIFIER},
                     expected_args=expected_args,
                     expected_kwargs=expected_kwargs)


class TestRefreshTask(testtools.TestCase):
    def test_basic(self):
        sot = task.RefreshTask()
        self.assertEqual('refreshTask', sot.resource_key)
        self.assertEqual('refreshTasks', sot.resources_key)
        self.assertEqual('/cdn/refreshtasks', sot.base_path)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

    def test_make_it(self):
        body = {
            "id": "8a29d3f05d0c9fc3015d0ca1bdae0005",
            "taskType": "refresh",
            "status": "task_inprocess",
            "total": 4,
            "processing": 0,
            "succeed": 0,
            "failed": 0,
            "create_time": 1499155459813,
            "urls": ["https://www.xxx.com/test.jpg",
                     "http://www.xxx.com/test2.jpg"]
        }
        sot = task.RefreshTask(**body)
        self.assertEqual(body['id'], sot.id)
        self.assertEqual(body['taskType'], sot.task_type)
        self.assertEqual(body['status'], sot.status)
        self.assertEqual(body['total'], sot.total)
        self.assertEqual(body['processing'], sot.processing)
        self.assertEqual(body['succeed'], sot.succeeded)
        self.assertEqual(body['failed'], sot.failed)
        self.assertItemsEqual(body['urls'], sot.urls)
        self.assertEqual(body['create_time'], sot.created_at)

    def test_make_request(self):
        body = {
            "type": "file",
            "urls": ["https://www.xxx.com/test.jpg",
                     "http://www.xxx.com/test2.jpg"]
        }
        sot = task.RefreshTask(**body)
        self.assertEqual(body['type'], sot.type)
        self.assertItemsEqual(body['urls'], sot.urls)


class TestPreheatTask(testtools.TestCase):
    def test_basic(self):
        sot = task.PreheatTask()
        self.assertEqual('preheatingTask', sot.resource_key)
        self.assertEqual('preheatingTasks', sot.resources_key)
        self.assertEqual('/cdn/preheatingtasks', sot.base_path)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

    def test_make_it(self):
        body = {
            "id": "8a29d3f05d0c9fc3015d0ca1bdae0005",
            "task_type": "refresh",
            "status": "task_inprocess",
            "total": 4,
            "processing": 0,
            "succeed": 0,
            "failed": 0,
            "create_time": 1499155459813,
            "urls": ["https://www.xxx.com/test.jpg",
                     "http://www.xxx.com/test2.jpg"]
        }
        sot = task.PreheatTask(**body)
        self.assertEqual(body['id'], sot.id)
        self.assertEqual(body['task_type'], sot.task_type)
        self.assertEqual(body['status'], sot.status)
        self.assertEqual(body['total'], sot.total)
        self.assertEqual(body['processing'], sot.processing)
        self.assertEqual(body['succeed'], sot.succeeded)
        self.assertEqual(body['failed'], sot.failed)
        self.assertItemsEqual(body['urls'], sot.urls)
        self.assertEqual(body['create_time'], sot.created_at)
