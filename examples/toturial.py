# Copyright 2017 HuaWei Tld
# Copyright 2017 OpenStack.org
#
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

from openstack import connection


# setup endpoint override for cloud services
os.environ.setdefault(
    'OS_CLOUD_EYE_ENDPOINT_OVERRIDE',
    'https://ces.eu-de.otc.t-systems.com/V1.0/%(project_id)s'
)
os.environ.setdefault(
    'OS_AUTO_SCALING_ENDPOINT_OVERRIDE',
    ('https://as.eu-de.otc.t-systems.com'
     '/autoscaling-api/v1/%(project_id)s')
)
os.environ.setdefault(
    'OS_DNS_ENDPOINT_OVERRIDE',
    'https://dns.eu-de.otc.t-systems.com'
)
os.environ.setdefault(
    'OS_VOLUME_BACKUP_ENDPOINT_OVERRIDE',
    'https://vbs.eu-de.otc.t-systems.com/v2/%(project_id)s'
)
os.environ.setdefault(
    'OS_LOAD_BALANCER_ENDPOINT_OVERRIDE',
    'https://elb.eu-de.otc.t-systems.com/v1.0/%(project_id)s'
)
os.environ.setdefault(
    'OS_MAP_REDUCE_ENDPOINT_OVERRIDE',
    'https://mrs.eu-de.otc.t-systems.com/v1.1/%(project_id)s'
)

# create connection
username = "replace-with-your-username"
password = "replace-with-your-password"
projectId = "d4f2557d248e4860829f5fef030b209c"
userDomainId = "bb42e2cd2b784ac4bdc350fb660a2bdb"
auth_url = "https://iam.eu-de.otc.t-systems.com/v3"
conn = connection.Connection(auth_url=auth_url,
                             user_domain_id=userDomainId,
                             project_id=projectId,
                             username=username,
                             password=password)

# call API
zones = conn.dns.zone.list()
print(list(zones))