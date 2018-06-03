from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql


# NOTE: this function must return a dictionary type
def post(request, connection):
    # connection = pymysql.connect() # DELETE this after done with coding

    try:
        __first_user = request['user_1']
        __second_user = request['user_2']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    __link = query_strings.link_friend.format[__second_user, __first_user, 'NULL', __first_user, __second_user, 'NULL']

    with connection.cursor() as cur:
        cur.execute(__link)
        connection.commit()

    body = Body()
    body.addParameter('message', 'friends.post has been called')
    return body
