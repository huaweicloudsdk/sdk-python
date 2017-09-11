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

"""
Managing smn

"""


def operate_topic(conn):
    topic_dict = {
        'name': 'labj',
        'display_name': 'djb',
    }

    tp = conn.smn.create_topic(**topic_dict)
    print(tp)

    update_dict = {
        'display_name': 'djbsbxxxxxxxx',
    }

    newtp = conn.smn.update_topic(tp, **update_dict)
    print(newtp)

    print("get topic from topic urn")
    gettp = conn.smn.get_topic(newtp.topic_urn)
    print(gettp)

    print("publish topic")
    msg_dict = {
        'message': "hello world!"
    }
    print("publish message")
    print(conn.smn.publish_topic(tp, **msg_dict))

    conn.smn.delete_topic(tp)

    print("get all topics with query")

    for t in conn.smn.topics(offset=0, limit=10):
        print(t)


def send_sms(conn):
    msg_dict = {
        'endpoint': '+12345678',
        'message': 'FYL',
        'sign_id': '94d3b63a5dfb475994d3ac34664e2346'
    }
    print(conn.direct_publish(**msg_dict))


def operate_topic_attr(conn):

    topic_dict = {
        'name': 'labj',
        'display_name': 'djb',
    }

    print("create a topic")
    tp = conn.smn.create_topic(**topic_dict)

    print("get topic attr of the topic")
    tpr = conn.smn.get_topic_attr(tp)

    print("topic attr is:")
    print(tpr)

    print("update a topic attr by attr name")
    attr_val_str = """{\"Version\": \"2016-09-07\"}"""
    print(conn.smn.update_topic_attr(tpr, 'access_policy', attr_val_str))

    print("delete topic access_policy attribute")
    conn.smn.delete_topic_attr(tpr, 'access_policy')

    print("delete all topic attrs of the topic")
    conn.smn.delete_topic_attrs(tp)
    print("delete the topic")
    conn.smn.delete_topic(tp)


def subscriptions(conn):
    print("list all subscriptions")
    for s in conn.smn.subscriptions(offset=0, limit=2):
        print(s)


def topic_subscriptions(conn):
    topic_dict = {
        'name': 'labj',
        'display_name': 'djb',
    }

    print("create a topic")
    tp = conn.smn.create_topic(**topic_dict)

    print("list specific topic subscriptions")
    for s in conn.smn.topic_subscriptions(tp.topic_urn, offset=0, limit=10):
        print(s)


def subscript_topic(conn):

    topic_dict = {
        'name': 'labj',
        'display_name': 'djb',
    }

    print("create a topic")
    tp = conn.smn.create_topic(**topic_dict)

    sub_dict = {
        'protocol': 'email',
        'endpoint': 'xxx@xxx.com',
        'remark': 'test',
    }

    sub = conn.smn.subscript_topic(tp, **sub_dict)
    print(sub)
    print("confirm subscription")
    print(conn.smn.confirm_subcription(sub, "token"))
    print("unsub")
    conn.smn.unsubscript_topic(sub.subscription_urn)
    print("delete the topic")
    conn.smn.delete_topic(tp)


def operate_template_message(conn):
    m_dict = {
        'message_template_name': 'testfoobarxxx',
        'protocol': "email",
        'content': 'what the fuck!'
    }
    update_dict = {
        'content': 'be civilization'
    }

    print("list all message templates")
    for m in conn.smn.message_templates(offset=0, limit=10):
        print(m)

    newm = conn.smn.create_message_template(**m_dict)
    print("created new template is:")
    print(newm)
    getm = conn.smn.get_message_template(newm.message_template_id)
    print("new template detail is:")
    print(getm)

    updatedm = conn.smn.update_message_template(getm, **update_dict)
    print("update the template to:")
    print(updatedm)
    print("delete template")
    conn.smn.delete_message_template(updatedm)
    for m in conn.smn.message_templates(offset=0, limit=10):
        print(m)
