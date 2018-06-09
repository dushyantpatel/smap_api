# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def put(request, query_str_param, connection):
    body = Body()
    body.addParameter('message', 'missions.put has been called')
    return body
