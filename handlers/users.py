from response_objects import *
from handlers.users_method import *


# list of valid methods for users
methods = {'GET': get,
           'POST': post,
           'PUT': put}


# handler for users
def handler(request, connection):
    """This function will handle all method requests for users"""
    method = request['httpMethod']
    status_code = 200
    header = Header()
    body = Body({})

    try:
        body = methods[method](request, connection)
    except KeyError:
        status_code = 501

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    res = Response(status_code, header.getHeader(), body.getBody())

    return res.getResponse()
