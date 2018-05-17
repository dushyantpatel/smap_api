# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def get(request, connection):
    body = Body()
    body.addParameter('message', 'plan.get has been called')
    return body
