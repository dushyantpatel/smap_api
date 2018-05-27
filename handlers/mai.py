from response_objects import *
from handlers.mai_method import *
import ast


# dictionary of valid methods for mai
methods = {'GET': get}


# handler for mai
def handler(event, connection):
    """This function will handle all method requests for mai"""
    method = event['httpMethod']
    status_code = 200
    header = Header()
    body = Body()

    try:
        body = methods[method](ast.literal_eval(event['body']), connection)
    except KeyError:
        status_code = 501

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    res = Response(status_code, header.getHeader(), body.getBody())

    return res.getResponse()
