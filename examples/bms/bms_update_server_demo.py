from openstack import connection
import os
import time

#os.environ.setdefault(
#    'OS_BMS_ENDPOINT_OVERRIDE',
#    'https://bms.cn-north-1.myhuaweicloud.com/v1/%(project_id)s')



username = "test_user"
password = "test_password"
projectId = "000efdc5f9064584b718b181df137bd7"
userDomainId = "49d5b5a8dbc04efa806afcc323d35880"
auth_url = "https://iam.cn-north-1.myhuaweicloud.com/v3"

conn = connection.Connection(auth_url=auth_url,
                             user_domain_id=userDomainId,
                             project_id=projectId,
                             username=username,
                             password=password)

def update_bare_metal_server(server_id, server_body):
    server_update = conn.compute.update_server(server_id, **server_body)
    print server_update

server_id = "d8bfd199-6b5b-45a9-86e4-31965924836c"

new_body = {
            "name": "test.bms_update_name"
        }
update_bare_metal_server(server_id, new_body)


