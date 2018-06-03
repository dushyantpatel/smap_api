# TODO - implementation
from response_objects.response_body import Body
from database_queries import *
from exceptions import *

# NOTE: this function must return a dictionary type
def get(request, connection):
    # connection = pymysql.connect() # DELETE this after done with coding
    try:
        first_user = request['user_1']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')
    try:
        link = query_strings.search_friends.format[user]
    except:
        raise HTTP_400_Exception('Invalid user(s)')

    with connection.cursor() as cur:
        cur.execute(link)
        connection.commit()
    body = Body()
    body.addParameter('message', 'friends.get has been called')
    return body
