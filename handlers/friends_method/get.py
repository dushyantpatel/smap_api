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

    __link = query_strings.search_friends.format[__user]

    with connection.cursor() as cur:
        cur.execute(__link)
        li = cur.fetchall()

    new_list = []
    for item in li:
        new_list.append(list(item))

    body = Body()
    body.addParameter('data', new_list)
    body.addParameter('message', 'friends.get has been called')
    return body
