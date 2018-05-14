from response_objects import *
from handlers.missions_method import *


# list of valid methods for missions
methods = {'GET': get,
           'POST': post,
           'PUT': put,
           'DELETE': delete}


# handler for missions
def handler(request, connection):
    """This function will handle all method requests for missions"""
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
