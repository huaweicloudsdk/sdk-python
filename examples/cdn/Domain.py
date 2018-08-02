#!/usr/bin/python
# coding=utf-8


import os
import sys
import time
from openstack import connection

os.environ.setdefault('OS_CDN_ENDPOINT_OVERRIDE', 'https://cdn.myhwclouds.com/v1.0')

username = "xxxxxxxxxxx"
password = "xxxxxxxxxxx"
projectId = "xxxxxxxxxxx"
userDomainId = "xxxxxxxxxxx"
auth_url = "https://iam.cn-north-1.myhuaweicloud.com/v3"

conn = connection.Connection(
    auth_url=auth_url,
    user_domain_id=userDomainId,
    project_id=projectId,
    username=username,
    password=password
)


def domain_create(domain_name):
    print('Create a new acceleration domain name: ')
    attrs = {
        'domain_name': domain_name,
        'business_type': 'web',
        'sources': [
            {
                'ip_or_domain': 'X.X.X.X',
                'origin_type': 'ipaddr',
                'active_standby': 1         # 1 means this source is active
            }
        ]
    }
    domain = conn.cdn.create_domain(**attrs)


def domains_query():
    print('List all domains:')
    for domain in conn.cdn.domains():
        print(domain)

    # Also support filtering by some attributes
    print('List all domains in "online" status: ')
    for domain in conn.cdn.domains(domain_status='online'):
        print(domain)

    for domain in conn.cdn.domains(business_type='web'):
        print(domain)

    # You can list domains by page.
    print('List 3rd and 4th domains: ')
    for domain in conn.cdn.domains(page_size=2, page_number=1):
        print(domain)


def domain_query_detail(domain_id):
    print('Get the domain detail:')
    domain = conn.cdn.get_domain(domain_id)
    print(domain)


def domain_disable_and_delete(domain_id):
    print('Delete the domain: ')
    # Disable the domain before deleting
    conn.cdn.disable_domain(domain_id)
    cnt = 300
    print('Waiting for domain disabled')
    while cnt:
        print('.')
        domain = conn.cdn.get_domain(domain_id)
        if domain.domain_status == 'offline':
            break
        else:
            time.sleep(1)
    if cnt:
        print('Deleted the domain.')
        conn.cdn.delete_domain(domain_id)
    else:
        print('Disable domain timeout')


if __name__ == "__main__":
    domain_name = 'cdn-python-sdk.example.com'
    domain_id = 'xxxxxxxxxxx'
    
    domain_create(domain_name)
    
    domains_query()
    
    domain_query_detail(domain_id)
    
    domain_disable_and_delete(domain_id)

