#!/usr/bin/python
# coding=utf-8


import os
import sys
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

def preheattask(preheatTask):
    print("preheat urls or dirs:")
    preheattask = conn.cdn.create_preheat_task(**preheatTask)
    print(preheattask)

if __name__ == "__main__":
    preheatTask={
        "urls": ["http://cdn-python-sdk.example.com/img/a7.jpg",
                 "http://cdn-python-sdk.example.com/js/plugins/"]
    }
    preheattask(preheatTask)

