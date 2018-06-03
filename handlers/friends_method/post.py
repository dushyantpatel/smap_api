# TODO - implementation
from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql


# NOTE: this function must return a dictionary type
def post(request, connection):
    # connection = pymysql.connect() # DELETE this after done with coding
    try:
        first_user = request['user_1']
        second_user = request['user_2']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')
    try:
        link = query_strings.link_friend.format[second_user, first_user, 'NULL', first_user, second_user, 'NULL']
    except:
        raise HTTP_400_Exception('Invalid user(s)')

    with connection.cursor() as cur:
        cur.execute(link)
        connection.commit()

    body = Body()
    body.addParameter('message', 'friends.post has been called')
    return body
