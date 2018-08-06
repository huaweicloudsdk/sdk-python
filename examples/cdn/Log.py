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


def list_logs(domain_name, today):
    #today = '1532620800000'
    logs = conn.cdn.logs(domain_name=domain_name, query_date=today, page_number=1, page_size=10)
    log_list = list(logs)
    print(log_list)
    # for log in conn.cdn.logs(domain_name=domain_name, query_date=today):
    #     print(log)

if __name__ == "__main__":
    today = int(time.time() * 1000) - 24 * 3600 * 1000
    domain = "cdn-python-sdk.example.com"
    list_logs(domain, today)


