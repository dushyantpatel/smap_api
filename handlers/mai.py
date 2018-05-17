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
