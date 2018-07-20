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


def test_show_all_rules(pl_id):
    rules = list(conn.network.rules(policy_id = pl_id))
    print 'rule numbers: ', len(rules)
    for rule in rules:
        print rule


def test_show_rule(rule_id, pl_id):
    print conn.network.get_rule(rule_id, pl_id)


def test_create_rule(pl_id):
    rule = conn.network.create_rule(policy_id = pl_id,
                                    type = 'HOST_NAME',
                                    compare_type = 'EQUAL_TO',
                                    value = 'www.test.com')
    return rule


def test_update_rule(rule_id, pl_id):
    data = {'policy_id':pl_id, 'cmpare_type':'EQUAL_TO', 'rule_value' : 'www.test-update.com'}
    rule = conn.network.update_rule(rule_id, **data)
    return rule


def test_delete_rule(rule_id, pl_id):
    conn.network.delete_rule(rule_id, pl_id)


if __name__ == "__main__":
    # policy without Domain Name
    policy_id = "9a6ea8f8-78ab-4ba3-8274-d1d05341565b"
    rule = test_create_rule(policy_id)
    rule_update = test_update_rule(rule.id, policy_id)
    test_show_rule(rule.id, policy_id)
    test_show_all_rules(policy_id)
    test_delete_rule(rule.id, policy_id)