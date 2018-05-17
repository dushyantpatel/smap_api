# TODO - implementation
from response_objects.response_body import Body


# NOTE: this function must return a dictionary type
def post(request, connection):
    body = Body()
    body.addParameter('message', 'plan.post has been called')
    return body
