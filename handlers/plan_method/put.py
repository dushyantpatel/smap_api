# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def put(request, connection):
    body = Body()
    body.addParameter('message', 'plan.put has been called')
    return body
