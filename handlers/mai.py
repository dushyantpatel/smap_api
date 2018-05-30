from response_objects import *
from handlers.mai_method import *
from exceptions import *
import ast


# dictionary of valid methods for mai
methods = {'GET': get}


# handler for mai
def handler(event, connection):
    """
    This function will handle all method requests for mai

    :param event: the api_call event dict object
    :param connection: an open connection to the database
    :return: the HTTP response object
    """

    method = event['httpMethod']
    status_code = 200
    details = 'Everything seems to be OK'
    header = Header()
    res_body = Body()

    try:
        req_body = "{}" if event['body'] is None else event['body']
        res_body = methods[method](ast.literal_eval(req_body), connection)
    except KeyError:
        status_code = 501
    except SyntaxError:
        status_code = 400
        details = 'Incorrect body format'
    except HTTP_204_Exception as ex:
        status_code = 204
        details = str(ex)
    except HTTP_400_Exception as ex:
        status_code = 400
        details = str(ex)

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    header.addParameter('details', details)
    res = Response(status_code, header.getHeader(), res_body.getBody())

    return res.getResponse()
