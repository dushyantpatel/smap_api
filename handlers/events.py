from response_objects import *
from handlers.events_method import *


# list of valid methods for events
methods = {'GET': get,
           'POST': post,
           'PUT': put,
           'DELETE': delete}


# handler for events
def handler(event, connection):
    """This function will handle all method requests for events"""
    method = event['httpMethod']
    status_code = 200
    header = Header()
    body = Body()

    try:
        body = methods[method](event, connection)
    except KeyError:
        status_code = 501

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    res = Response(status_code, header.getHeader(), body.getBody())

    return res.getResponse()
