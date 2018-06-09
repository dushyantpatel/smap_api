# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def delete(request, query_str_param, connection):
    body = Body()
    body.addParameter('message', 'events.delete has been called')
    return body
