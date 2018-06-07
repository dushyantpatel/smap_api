from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql


# NOTE: this function must return a dictionary type
def post(request, connection):

    try:
        __first_user = request['user_1']
        __second_user = request['user_2']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    # __first_user sends request to __second_user
    __link = query_strings.friend_requested.format(__first_user, __second_user, 'NULL')
    with connection.cursor() as cur:
        try:
            cur.execute(__link)
            connection.commit()
        except pymysql.err.IntegrityError:
            raise HTTP_204_Exception('User not found')

    body = Body()
    return body
