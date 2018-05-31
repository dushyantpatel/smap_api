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
except pymysql.err.Error as ex:
    template = "ERROR: {0} - Could not connect to MySql instance \n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    logger.error(message)
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

# connection = None  # This is just for testing - uncomment the above code and delete this line after testing
# valid api resources
resources = {"/mai": mai.handler,
             "/events": events.handler,
             "/missions": missions.handler,
             "/plan": plan.handler,
             "/users": users.handler,
             "/friends": friends.handler}


# main handler for any API call
def main_handler(event, context):
    """This function handles all API calls"""

    path = event['path']

    try:
        handler = resources[path]
    except KeyError:
        status_code = 501
        header = Header()
        header.addParameter('status', status_code)
        header.addParameter('message', responseCodeDescription(status_code))
        res = Response(status_code, header.getHeader(), Body().getBody())
        return res.getResponse()

    return handler(event, connection)  # call appropriate handler
