import sys
import logging
import rds_config
import pymysql
from handlers import *
from response_objects import *

# rds settings
rds_host = rds_config.db_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

# logger settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# connect to database
try:
    connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

# valid api resources
resources = {"/mai": mai.handler,
             "/events": events.handler,
             "/missions": missions.handler,
             "/plan": plan.handler,
             "/users": users.handler}


# main handler for any API call
def main_handler(request, context):
    """This function handles all API calls"""

    path = request['path']

    try:
        handler = resources[path]
    except KeyError:
        status_code = 501
        header = Header()
        header.addParameter('status', responseCodeDescription(status_code))
        res = Response()
        res.setStatusCode(status_code)
        res.setHeaders(header.getHeader())
        res.setBody(Body())
        return res.getResponse()

    return handler(request, connection)  # call appropriate handler
