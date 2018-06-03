# TODO - implementation
from response_objects.response_body import Body
import pymysql
from database_queries import *
from exceptions import *
"""
First: 
Get events from data that match descrip/var passed by front end put into body to return
Get all events with passed in category
Generally by any event variable
var_list = list(var)
body.addPara('data', var_list)
"""

# NOTE: this function must return a dictionary type
def get(request, connection):
    """
    #required variable
    zip = None
    #optional variables
    catagory = None
    name = None
       try:
        zip = request['zip']
    except KeyError:
        raise HTTP_204_Exception("Missing a required field")
    try:
        name = request['name']
    except KeyError:
        pass
    if name == None:
        try:
            catagory = request['catagory']
        except KeyError:
            pass
        if catagory == None:
   """
    #Get all events from the data_base
    with connection.cursor() as cur:
        cur.execute(query_strings.search_all_events)
        __events = cur.fetchall()
    body = Body()
    body.addParameter('events', __events)
    return body
