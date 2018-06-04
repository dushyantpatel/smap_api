from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql

# NOTE: this function must return a dictionary type
def get(request, connection):
    #connection = pymysql.connect() # DELETE this after done with coding

    try:
        __user = request['user']
        __friend_status = request['status']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    if __friend_status == 'friends':
        __link = query_strings.search_friends.format[__user]
    elif __friend_status == 'responses':
        __link = query_strings.search_pending_requests[__user]
    elif __friend_status == 'requests':
        __link = query_strings.search_requests_sent[__user]

    try:
        with connection.cursor() as cur:
            cur.execute(__link)
            li = cur.fetchall()
    except pymysql.err.IntegrityError:
        raise HTTP_204_Exception('User not found')

    new_list = []
    for item in li:
        new_list.append(list(item))

    body = Body()
    body.addParameter('data', new_list)
    return body