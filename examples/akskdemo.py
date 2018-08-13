#encoding=utf-8

import sys
from openstack import connection
from openstack import utils


utils.enable_logging(debug = True, stream = sys.stdout)

projectId = "***"
domain = '***'
region='***'
AK = '***'
SK = '***'

conn = connection.Connection(
              project_id=projectId,
              domain=domain,
              region=region,
              ak = AK,
              sk = SK
             )

def test_compute():
    servers = conn.compute.servers()
    for server in servers:
        print server


if __name__ == "__main__":
    test_compute()