# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def delete(request, connection):
    body = Body()
    body.addParameter('message', 'plan.delete has been called')
    return body
