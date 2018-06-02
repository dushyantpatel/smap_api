# TODO - implementation
from response_objects.response_body import Body
"""
First: put: update 
"""

# NOTE: this function must return a dictionary type
def put(request, connection):
    body = Body()
    body.addParameter('message', 'events.put has been called')
    return body
