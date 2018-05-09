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

from openstack.cdn.v1 import domain

IDENTIFIER = 'ff80808260454e2601604eece675107b'
EXAMPLE = {
    "sources": [
        {
            "domain_id": "ff80808260454e2601604eece675107b",
            "ip_or_domain": "1.2.3.4",
            "origin_type": "ipaddr",
            "active_standby": 1
        }
    ],
    "id": "ff80808260454e2601604eece675107b",
    "user_domain_id": "38de6682b3024a1497d249ea45024dcb",
    "domain_name": "obs-9b234.obs.cn-north-1.myhwclouds.com",
    "business_type": "web",
    "cname": "cdn-9b234.cn-north-1.myhwclouds.com.c.cdnhwc1.com",
    "domain_status": "configuring",
    "https_status": None,
    "description": None,
    "create_time": 1513152634467,
    "modify_time": 1513152634467,
    "domain_origin_host": {
        "domain_id": "ff80808260454e2601604eece675107b",
        "origin_host_type": "customize",
        "customize_domain": "test961.donyd.com"
    },
    "disabled": 0,
    "locked": 1
}


class TestDomain(testtools.TestCase):
    def test_basic(self):
        sot = domain.Domain()
        self.assertEqual('domain', sot.resource_key)
        self.assertEqual('domains', sot.resources_key)
        self.assertEqual('/cdn/domains', sot.base_path)
        self.assertEqual('cdn', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({'page_size': 'page_size',
                              'page_number': 'page_number',
                              'domain_name': 'domain_name',
                              'business_type': 'business_type',
                              'domain_status': 'domain_status'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = domain.Domain(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['user_domain_id'], sot.user_domain_id)
        self.assertEqual(EXAMPLE['domain_name'], sot.domain_name)
        self.assertEqual(EXAMPLE['business_type'], sot.business_type)
        self.assertEqual(EXAMPLE['cname'], sot.cname)
        self.assertEqual(EXAMPLE['domain_status'], sot.domain_status)
        self.assertIsNone(sot.https_status)
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
        self.assertEqual(EXAMPLE['modify_time'], sot.modified_at)
        self.assertFalse(sot.is_disabled)
        self.assertTrue(sot.is_locked)
        self.assertItemsEqual(EXAMPLE['sources'], sot.sources)
        self.assertDictEqual(EXAMPLE['domain_origin_host'],
                             sot.domain_origin_host)

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
        sot = domain.Domain(id=IDENTIFIER)
        url = 'cdn/domains/%s/detail' % IDENTIFIER
        expected_args = [url]
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }

        self._verify(sot.get, 'get',
                     mock_json={'domain': {'id': IDENTIFIER}},
                     expected_args=expected_args,
                     expected_kwargs=expected_kwargs)

    def test_set_sources(self):
        req = {
            'ip_or_domain': '1.2.3.4',
            'origin_type': 'ipaddr',
            'active_standby': 1
        }
        source = {
            'domain_id': 'id',
            'ip_or_domain': '1.2.3.4',
            'origin_type': 'ipaddr',
            'active_standby': 1
        }
        body = {
            'origin': {
                'sources': [source]
            }
        }

        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/origin'
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
            'json': {'origin': {'sources': [req]}}
        }
        self._verify(sot.set_sources, 'put',
                     mock_json=body,
                     method_args=[req],
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)
        self.assertItemsEqual([source], sot.sources)

    def test_enable(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/enable'
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
        }
        self._verify(sot.enable, 'put',
                     mock_json={'domain': {'id': 'id', 'disabled': 0}},
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)
        self.assertFalse(sot.is_disabled)

    def test_disable(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/disable'
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
        }
        self._verify(sot.disable, 'put',
                     mock_json={'domain': {'id': 'id', 'disabled': 1}},
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)
        self.assertTrue(sot.is_disabled)

    def test_set_origin_host(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/originhost'
        origin_host = {
            'origin_host_type': 'customize',
            'customize_domain': 'origin.example.com'
        }
        body = {
            'origin_host': {
                'domain_id': 'id',
                'origin_host_type': 'customize',
                'customize_domain': 'origin.example.com'
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
            'json': {'origin_host': origin_host}
        }
        self._verify(sot.set_origin_host, 'put',
                     mock_json=body,
                     method_kwargs=origin_host,
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)
        self.assertDictEqual(body['origin_host'], sot.domain_origin_host)

    def test_get_origin_host(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/originhost'
        body = {
            'origin_host': {
                'domain_id': 'id',
                'origin_host_type': 'customize',
                'customize_domain': 'origin.example.com'
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }
        actual_result = self._verify(sot.get_origin_host, 'get',
                                     mock_json=body,
                                     expected_args=[url],
                                     expected_kwargs=expected_kwargs)
        self.assertDictEqual(body['origin_host'], actual_result)

    def test_set_referer(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/referer'
        body = {
            'referer': {
                'referer_type': 1,
                'referer_list': 'www1.example.com;www2.fake.com',
                'include_empty': False
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
            'json': body
        }
        self._verify(sot.set_referer, 'put',
                     mock_json=body,
                     method_kwargs=body['referer'],
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)

    def test_get_referer(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/referer'
        body = {
            'referer': {
                'referer_type': 1,
                'referer_list': 'www1.example.com;www2.fake.com',
                'include_empty': False
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }
        actual_result = self._verify(sot.get_referer, 'get',
                                     mock_json=body,
                                     expected_args=[url],
                                     expected_kwargs=expected_kwargs)
        self.assertDictEqual(body['referer'], actual_result)

    def test_set_cache_rules(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/cache'
        cache_config = {
            "ignore_url_parameter": False,
            "rules": [
                {
                    "rule_type": 1,
                    "content": ".jpg;.png",
                    "ttl": 2,
                    "ttl_type": 3,
                    "priority": 1
                }
            ]
        }
        body = {
            "cache_config": {
                "ignore_url_parameter": False,
                "ignore_cache_control": True,
                "rules": [
                    {
                        "rule_type": 1,
                        "content": ".jpg;.png",
                        "ttl": 2,
                        "ttl_type": 3,
                        "priority": 1
                    }
                ]
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
            'json': {'cache_config': cache_config}
        }
        self._verify(sot.set_cache_rules, 'put',
                     mock_json=body,
                     method_kwargs=cache_config,
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)

    def test_get_cache_rules(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/cache'
        body = {
            "cache_config": {
                "ignore_url_parameter": False,
                "ignore_cache_control": True,
                "rules": [
                    {
                        "rule_type": 1,
                        "content": ".jpg;.png",
                        "ttl": 2,
                        "ttl_type": 3,
                        "priority": 1
                    }
                ]
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }
        actual_result = self._verify(sot.get_cache_rules, 'get',
                                     mock_json=body,
                                     expected_args=[url],
                                     expected_kwargs=expected_kwargs)
        self.assertDictEqual(body['cache_config'], actual_result)

    def test_set_https(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/https-info'
        https = {
            "force_redirect_https": 0,
            "https_status": 2,
            "cert_name": "cdn_test_cert",
            "certificate": "BEGIN CERTIFICATE-END CERTIFICATE",
            "private_key": "BEGIN RSA PRIVATE KEY-END RSA PRIVATE KEY"
        }
        body = {
            "https": {
                "force_redirect_https": 0,
                "https_status": 1,
                "cert_name": "cdn_test_cert",
                "certificate": "-----BEGIN CERTIFICATE-END CERTIFICATE-----"
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None,
            'json': {'https': https}
        }
        self._verify(sot.set_https, 'put',
                     mock_json=body,
                     method_kwargs=https,
                     expected_args=[url],
                     expected_kwargs=expected_kwargs)

    def test_get_https(self):
        sot = domain.Domain(id='id')
        url = 'cdn/domains/id/https-info'
        body = {
            "https": {
                "force_redirect_https": 0,
                "https_status": 1,
                "cert_name": "cdn_test_cert",
                "certificate": "-----BEGIN CERTIFICATE-END CERTIFICATE-----"
            }
        }
        expected_kwargs = {
            'endpoint_filter': sot.service,
            'endpoint_override': None
        }
        actual_result = self._verify(sot.get_https, 'get',
                                     mock_json=body,
                                     expected_args=[url],
                                     expected_kwargs=expected_kwargs)
        self.assertDictEqual(body['https'], actual_result)
