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

from openstack.cdn.v1 import _proxy
from openstack.cdn.v1 import domain
from openstack.cdn.v1 import log
from openstack.cdn.v1 import statistic
from openstack.cdn.v1 import task
from openstack.tests.unit import test_proxy_base2


class TestProxy(test_proxy_base2.TestProxyBase):
    def setUp(self):
        super(TestProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_domains(self):
        kwargs = {'page_size': 100, 'page_number': 1}
        self.verify_list(self.proxy.domains, domain.Domain,
                         paginated=True,
                         expected_kwargs=kwargs)

    def test_domains_with_pagination(self):
        kwargs = {'page_size': 10, 'page_number': 2}
        self.verify_list(self.proxy.domains, domain.Domain,
                         paginated=True,
                         method_kwargs=kwargs,
                         expected_kwargs=kwargs)

    def test_domains_with_query_params(self):
        kwargs = {'domain_name': '1', 'business_type': '2',
                  'domain_status': '3'}
        expected_kwargs = {'page_size': 100, 'page_number': 1}
        expected_kwargs.update(**kwargs)
        self.verify_list(self.proxy.domains, domain.Domain,
                         paginated=True,
                         method_kwargs=kwargs,
                         expected_kwargs=expected_kwargs)

    def test_create_domain(self):
        attrs = {
            "domain_name": "cdn-9b234.cn-north-1.myhwclouds.com",
            "business_type": "web",
            "sources": [
                {
                    "ip_or_domain": "1.2.3.4",
                    "origin_type": "ipaddr",
                    "active_standby": 1
                }
            ]
        }
        self.verify_create(self.proxy.create_domain, domain.Domain,
                           method_kwargs=attrs,
                           expected_kwargs=attrs)

    def test_get_domain(self):
        self.verify_get(self.proxy.get_domain, domain.Domain)

    def test_delete_domain(self):
        self.verify_delete(self.proxy.delete_domain, domain.Domain, False,
                           expected_kwargs={'has_body': True})

    def test_delete_domain_ignore(self):
        self.verify_delete(self.proxy.delete_domain, domain.Domain, True,
                           expected_kwargs={'has_body': True})

    def test_set_domain_sources(self):
        domain = 'id'
        source = {
            "ip_or_domain": "1.2.3.4",
            "origin_type": "ipaddr",
            "active_standby": 1
        }
        self._verify("openstack.cdn.v1.domain.Domain.set_sources",
                     self.proxy.set_domain_sources,
                     method_args=[domain, source],
                     expected_args=[source])

    def test_enable_domain(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.enable",
                     self.proxy.enable_domain,
                     method_args=[domain])

    def test_disable_domain(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.disable",
                     self.proxy.disable_domain,
                     method_args=[domain])

    def test_set_domain_origin_host(self):
        domain = 'id'
        attrs = {
            "origin_host_type": "customize",
            "customize_domain": "cdn-9b234.cn-north-1.myhwclouds.com"
        }
        self._verify("openstack.cdn.v1.domain.Domain.set_origin_host",
                     self.proxy.set_domain_origin_host,
                     method_args=[domain],
                     method_kwargs=attrs,
                     expected_kwargs=attrs)

    def test_get_domain_origin_host(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.get_origin_host",
                     self.proxy.get_domain_origin_host,
                     method_args=[domain])

    def test_set_domain_referer(self):
        domain = 'id'
        attrs = {
            "referer_type": 1,
            "referer_list": "www.xxx.com;www.xxx2.com",
            "include_empty": False
        }
        self._verify("openstack.cdn.v1.domain.Domain.set_referer",
                     self.proxy.set_domain_referer,
                     method_args=[domain],
                     method_kwargs=attrs,
                     expected_kwargs=attrs)

    def test_get_domain_referer(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.get_referer",
                     self.proxy.get_domain_referer,
                     method_args=[domain])

    def test_set_domain_cache_rules(self):
        domain = 'id'
        attrs = {
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
        self._verify("openstack.cdn.v1.domain.Domain.set_cache_rules",
                     self.proxy.set_domain_cache_rules,
                     method_args=[domain],
                     method_kwargs=attrs,
                     expected_kwargs=attrs)

    def test_get_domain_cache_rules(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.get_cache_rules",
                     self.proxy.get_domain_cache_rules,
                     method_args=[domain])

    def test_set_domain_https(self):
        domain = 'id'
        attrs = {
            "force_redirect_https": 0,
            "https_status": 2,
            "cert_name": "cdn_test_cert",
            "certificate": "BEGIN CERTIFICATEEND CERTIFICATE",
            "private_key": "BEGIN RSA PRIVATE KEYEND RSA PRIVATE KEY"
        }
        self._verify("openstack.cdn.v1.domain.Domain.set_https",
                     self.proxy.set_domain_https,
                     method_args=[domain],
                     method_kwargs=attrs,
                     expected_kwargs=attrs)

    def test_get_domain_https(self):
        domain = 'id'
        self._verify("openstack.cdn.v1.domain.Domain.get_https",
                     self.proxy.get_domain_https,
                     method_args=[domain])

    def test_tasks(self):
        kwargs = {'page_size': 100, 'page_number': 1}
        self.verify_list(self.proxy.tasks, task.Task,
                         paginated=True,
                         expected_kwargs=kwargs)

    def test_tasks_with_pagination(self):
        kwargs = {'page_size': 10, 'page_number': 2}
        self.verify_list(self.proxy.tasks, task.Task,
                         paginated=True,
                         method_kwargs=kwargs,
                         expected_kwargs=kwargs)

    def test_tasks_with_query_params(self):
        kwargs = {'status': '1', 'start_date': '2',
                  'end_date': '3', 'order_field': '4',
                  'order_type': '5', 'user_domain_id': '6'}
        expected_kwargs = {'page_size': 100, 'page_number': 1}
        expected_kwargs.update(**kwargs)
        self.verify_list(self.proxy.domains, domain.Domain,
                         paginated=True,
                         method_kwargs=kwargs,
                         expected_kwargs=expected_kwargs)

    def test_get_task(self):
        self.verify_get(self.proxy.get_task, task.Task)

    def test_create_refresh_task(self):
        attrs = {
            "type": "file",
            "urls": ["https://www.xxx.com/test.jpg",
                     "http://www.xxx.com/test2.jpg"]
        }
        self.verify_create(self.proxy.create_refresh_task, task.RefreshTask,
                           method_kwargs=attrs,
                           expected_kwargs=attrs)

    def test_create_preheat_task(self):
        attrs = {
            "urls": ["http://www.xxx.com/test15.jpg",
                     "https://www.xxx.cn/test/di.png",
                     ]
        }
        self.verify_create(self.proxy.create_preheat_task, task.PreheatTask,
                           method_kwargs=attrs,
                           expected_kwargs=attrs)

    def test_logs(self):
        args = ['domain_name', 'epoch_time']
        expected_kwargs = {'page_size': 100, 'page_number': 1,
                           'domain_name': 'domain_name',
                           'query_date': 'epoch_time',
                           'paginated': True}
        self.verify_list(self.proxy.logs, log.Log,
                         paginated=True,
                         method_args=args,
                         expected_kwargs=expected_kwargs)

    def test_query_network_traffic(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain'
        }
        self._verify("openstack.cdn.v1.statistic.NetworkTraffic.query",
                     self.proxy.query_network_traffic,
                     method_kwargs=query,
                     expected_kwargs=query)

    def test_query_network_traffic_detail(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain',
            'interval': 300
        }
        self._verify("openstack.cdn.v1.statistic.NetworkTrafficDetail.query",
                     self.proxy.query_network_traffic_detail,
                     method_kwargs=query,
                     expected_kwargs=query)

    def test_query_bandwidth_peak(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain'
        }
        self._verify("openstack.cdn.v1.statistic.BandwidthPeak.query",
                     self.proxy.query_bandwidth_peak,
                     method_kwargs=query,
                     expected_kwargs=query)

    def test_query_bandwidth(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain',
            'interval': 300
        }
        self._verify("openstack.cdn.v1.statistic.BandwidthDetail.query",
                     self.proxy.query_bandwidth,
                     method_kwargs=query,
                     expected_kwargs=query)

    def test_query_summary(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain',
            'stat_type': 'flux',
            'service_area': 'mainland_china'
        }
        self._verify("openstack.cdn.v1.statistic.ConsumptionSummary.query",
                     self.proxy.query_summary,
                     method_kwargs=query,
                     expected_kwargs=query)

    def test_query_summary_detail(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain',
            'interval': 300,
            'stat_type': 'flux',
            'service_area': 'mainland_china'
        }
        self._verify(
            "openstack.cdn.v1.statistic.ConsumptionSummaryDetail.query",
            self.proxy.query_summary_detail,
            method_kwargs=query,
            expected_kwargs=query)

    def test_summaries(self):
        query = {
            'start_time': 1,
            'end_time': 2,
            'domain_name': 'domain',
            'interval': 300,
            'stat_type': 'flux',
            'service_area': 'mainland_china'
        }
        self.verify_list(self.proxy.summaries,
                         statistic.ConsumptionSummaryByDomain,
                         method_kwargs=query,
                         expected_kwargs=query)
