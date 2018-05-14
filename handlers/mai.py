from response_objects import *
from handlers.mai_method import *


# dictionary of valid methods for mai
methods = {'GET': get}


# handler for mai
def handler(request, connection):
    """This function will handle all method requests for mai"""
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
