from response_objects.response_body import Body
from exceptions import *
from database_queries import *
import pymysql


# NOTE: this function must return a dictionary type
def put(request, connection):

    try:
        __first_user = request['user1']
        __second_user = request['user2']
        __action = request['action']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    # __first_user --> action --> __second_user
    if __action == 'accept':
        __link = query_strings.friend_request_accepted.format(__second_user, __first_user, __first_user, __second_user)
    elif __action == 'decline':
        __link = query_strings.friend_request_rejected.format(__second_user, __first_user)
    else:
        raise HTTP_400_Exception('Invalid action field - ' + __action)

    try:
        with connection.cursor() as cur:
            cur.execute(__link)
            connection.commit()
    except pymysql.err.IntegrityError:
        raise HTTP_204_Exception('User not found')

    body = Body()
    return body
