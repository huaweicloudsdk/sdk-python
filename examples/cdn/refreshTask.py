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

def refreshTask(refreshTask):
    print("refresh files or dirs:")
    refreshtask = conn.cdn.create_refresh_task(**refreshTask)
    print(refreshtask)



if __name__ == "__main__":
    refreshFileTask={
        "type": "file",
        "urls": ["http://cdn-python-sdk.example.com/img/a5.jpg",
                 "http://cdn-python-sdk.example.com/img/a7.jpg"]
    }
    refreshDirTask={
        "type": "directory",
        "urls": ["http://cdn-python-sdk.example.com/img/",
                "http://cdn-python-sdk.example.com/js/plugins/"]
    }
    refreshTask(refreshFileTask)
    refreshTask(refreshDirTask)

