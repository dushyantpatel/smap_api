import pymysql

from response_objects.response_body import Body
from database_queries import *
from exceptions import *

# NOTE: this function must return a dictionary type
def get(request, query_str_param, connection):

    try:
        name = request['name']
        searchQuery = query_strings.search_for_mission.format(name)
    except KeyError:
        searchQuery = query_strings.search_all_missions


    with connection.cursor() as cur:
        try:
            cur.execute(searchQuery)
            missions = cur.fetchall()
        except pymysql.err.IntegrityError:
            raise HTTP_204_Exception('User not found')


    body = Body()
    body.addParameter('missions', missions)
    body.addParameter('message', 'missions.get has been called')
    return body
