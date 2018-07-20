#!/usr/bin/python
# coding=utf-8


import sys
from openstack import connection
from openstack import utils

# utils.enable_logging(debug=True, stream=sys.stdout)

username = "xxxxxxxxxxx"
password = "xxxxxxxxxxx"
projectId = "xxxxxxxxxxx"
userDomainId = "xxxxxxxxxx"
auth_url = "xxxxxxxxxx"

conn = connection.Connection(
    auth_url=auth_url,
    user_domain_id=userDomainId,
    project_id=projectId,
    username=username,
    password=password
)


def test_show_all_pool():
    pos = list(conn.network.pools())
    print "pool numbers: ", len(pos)
    for p in pos:
        print p


def test_show_pool(pool_id):
    pool = conn.network.get_pool(pool_id)
    print pool


def test_create_pool(ls_or_lb_id):
    p = conn.network.create_pool(lb_algorithm="LEAST_CONNECTIONS",
                                 protocol = "TCP",
                                 listener_id = ls_or_lb_id,
                                 name = "pool-test",
                                 description="this is test pool"
                                 )
    return p


def test_update_pool(pool_id):
    _pool = conn.network.update_pool(pool_id, description="this is test pool",
                                     name = "test update pool",
                                     lb_algorithm = "SOURCE_IP",
                                     session_persistence = { 'type': 'SOURCE_IP'})
    return _pool


def test_delete_pool(pool_id):
    conn.network.delete_pool(pool_id)


if __name__ == "__main__":
    # listener id which is not using default pool
    ls_id = "3ab18a77-852e-4517-8127-2d0ef4412c1c"
    pool = test_create_pool(ls_id)
    test_update_pool(pool.id)
    test_show_pool(pool.id)
    test_show_all_pool()
    test_delete_pool(pool.id)