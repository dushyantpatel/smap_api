# TODO - implementation
from response_objects.response_body import Body
from database_queries import *
from exceptions import *


# NOTE: this function must return a dictionary type
def get(request, connection):
    #Get all events from the data_base
    with connection.cursor() as cur:
        cur.execute(query_strings.search_all_events)
        __events = cur.fetchall()
    body = Body()
    body.addParameter('events', __events)
    return body
