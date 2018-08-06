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


def test_show_all_l7policy():
    pls = list(conn.network.poliycies())
    print 'l7policy numbers: ', len(pls)
    for pl in pls:
        print pl


def test_show_l7policy(policy_id):
    print conn.network.get_policy(policy_id)


def test_create_l7policy(lb_id):
    _ls = conn.network.create_listener(protocol_port = '24',
                                       protocol = 'HTTP',
                                       loadbalancer_id = lb_id)
    _pool = conn.network.create_pool(lb_algorithm="LEAST_CONNECTIONS",
                                     protocol = "HTTP",
                                     loadbalancer_id = lb_id)
    _pl = conn.network.create_policy(action = 'REDIRECT_TO_POOL',
                                     listener_id = _ls.id,
                                     redirect_pool_id = _pool.id,
                                     )
    return _pl


def test_update_l7policy(policy_id):
    pl = conn.network.update_policy(policy_id,
                                    name = 'pl-update-test',
                                    description = 'this is a test')
    return pl


def test_delete_l7policy(policy_id):
    conn.network.delete_policy(policy_id)


if __name__ == "__main__":
    lb_id = "3784fefc-24da-49a2-9463-b2b751090755"
    l7policy = test_create_l7policy(lb_id)
    l7policy_update = test_update_l7policy(l7policy.id)
    test_show_l7policy(l7policy_update.id)
    test_show_all_l7policy()
    test_delete_l7policy(l7policy_update.id)