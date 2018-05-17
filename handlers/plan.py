from response_objects import *
from handlers.events_method import *


# list of valid methods for plan
methods = {'GET': get,
           'POST': post,
           'PUT': put,
           'DELETE': delete}


# handler for plan
def handler(request, connection):
    """This function will handle all method requests for plan"""
    method = request['httpMethod']
    status_code = 200
    header = Header()
    body = Body()

    try:
        body_content = methods[method](request, connection)
        body.setBody(body_content)
    except KeyError:
        status_code = 501

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    res = Response(status_code, header.getHeader(), body)

    return res.getResponse()
