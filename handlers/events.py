from response_objects import *
from handlers.events_method import *
from exceptions import *
import json


# dictionary of valid methods for events
methods = {'GET': get,
           'POST': post,
           'PUT': put,
           'DELETE': delete}


# handler for events
def handler(event, connection):
    """
    This function will handle all method requests for events

    :param event: the api_call event dict object
    :param connection: an open connection to the database
    :return: the HTTP response object
    """

    method = event['httpMethod']
    status_code = 201
    details = 'Everything seems to be OK'
    header = Header()
    res_body = Body()

    try:
        req_body = "{}" if event['body'] is None else event['body']
        query_str_param = event['queryStringParameters']
        res_body = methods[method](json.loads(req_body), query_str_param, connection)
        if method == 'GET':
            status_code = 200
    except KeyError:
        status_code = 501
        details = 'The ' + method + ' method has not been implemented.'
    except SyntaxError:
        status_code = 400
        details = 'Incorrect body format'
    except HTTP_204_Exception as ex:
        status_code = 204
        details = str(ex)
    except HTTP_400_Exception as ex:
        status_code = 400
        details = str(ex)
    except Exception as ex:
        status_code = 520
        details = 'ERROR type: {0}. \n{1!r} \n please record details of your API call and let the API developer know.'
        details = details.format(type(ex).__name__, ex.args)

    header.addParameter('status', status_code)
    header.addParameter('message', responseCodeDescription(status_code))
    header.addParameter('details', details)
    res = Response(status_code, header.getHeader(), res_body.getBody())

    return res.getResponse()
