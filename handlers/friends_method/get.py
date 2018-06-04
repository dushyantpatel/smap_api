from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql


# NOTE: this function must return a dictionary type
def get(request, connection):

    try:
        __user = request['user']
        __friend_status = request['status']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    if __friend_status == 'friends':
        __link = query_strings.search_friends.format(__user)
    elif __friend_status == 'responses':
        __link = query_strings.search_pending_requests.format(__user)
    elif __friend_status == 'requests':
        __link = query_strings.search_requests_sent.format(__user)
    else:
        raise HTTP_400_Exception('Invalid friend status')

    with connection.cursor() as cur:
        try:
            cur.execute(__link)
            li = cur.fetchall()
        except pymysql.err.IntegrityError:
            raise HTTP_204_Exception('User not found')

    new_list = []
    for item in li:
        usr = dict()
        usr['user_id'] = item[0]
        usr['display_name'] = item[1]
        usr['profile_pic'] = item[2]
        usr['email'] = item[3]
        usr['first_name'] = item[4]
        usr['last_name'] = item[5]
        usr['mission_curator'] = item[6]
        usr['birthday'] = item[7]
        usr['location'] = item[8]
        new_list.append(usr)

    body = Body()
    body.addParameter('data', new_list)
    return body
