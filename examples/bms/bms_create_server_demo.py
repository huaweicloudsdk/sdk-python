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

def create_bare_metal_server_prepaid():
    data = {
        "availability_zone": "cn-north-1a",
        "name": "test_bare_metal_server",
        "imageRef": "766a545a-02e1-433e-b1d1-733b5dc95e94",
        "metadata": {
             "op_svc_userid": "d2e6e8d7c08841ba9d2ebe0d5dbd7a0c"
        },
        "flavorRef": "physical.s1.medium",
        "vpcid": "ddd56db4-e084-42d1-b0ff-fba1ed82abd0",
        "key_name" : "KeyPair-test",
        "nics": [
            {
                "subnet_id": "5be0ddfb-1445-495c-8beb-4222a9c98102"
            }
        ],
        "extendparam": {
            "chargingMode": "prePaid",
            "periodType": "month",
            "periodNum": 1,
            "isAutoRenew": "false",
            "isAutoPay": "false",
            "regionID": "cn-north-1"
        }
    }
    response = conn.bms.create_server(**data)
    orderId = response.order_id
    print orderId
	
create_bare_metal_server_prepaid()

