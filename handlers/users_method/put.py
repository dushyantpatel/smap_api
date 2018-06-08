# TODO - implementation
from response_objects.response_body import Body
from database_queries import *
from exceptions import *


# NOTE: this function must return a dictionary type
def put(request, query_str_param, connection):
    body = Body()
    body.addParameter('message', 'users.put has been called')
    return body
