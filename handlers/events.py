from response_objects import *
from handlers.events_method import *


# list of valid methods for events
methods = {'GET': get,
           'POST': post,
           'PUT': put,
           'DELETE': delete}


# handler for events
def handler(request, connection):
    """This function will handle all method requests for events"""
    method = request['httpMethod']
    status_code = 200
    header = Header()
    res = Response()
    body = Body()

    try:
        body_content = methods[method](request, connection)
        body.setBody(body_content)
    except KeyError:
        status_code = 501

    header.addParameter('status', responseCodeDescription(status_code))
    res.setHeaders(header.getHeader())
    res.setStatusCode(status_code)
    res.setBody(body)

    return res.getResponse()
