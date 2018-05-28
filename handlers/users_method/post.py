from response_objects.response_body import Body
from database_queries import *
from exceptions import *
import pymysql

# Initialize File variables
__first_name = ''
__last_name = ''
__display_name = ''
__email = ''
__profile_pic = ''
__mission_curator = 0
__birthday = ''
__location = None
__street = ''
__city = ''
__state = ''
__zip = 0
__country = ''
__latitude = 0
__longitude = 0


# NOTE: this function must return a dictionary type
def post(request, connection):
    """
    This method is used to make the POST request in for the /users resource

    :param request: the request_body dict object
    :param connection: the open connection to the MySQL database
    :return: the response body
    """

    set_variables(request)

    db_add_user = get_add_user_command(connection)

    # add new user to the database
    with connection.cursor() as cur:
        cur.execute(db_add_user)
        connection.commit()

    body = Body()
    body.addParameter('message', 'users.post has been called')
    return body


def get_add_user_command(connection):
    """
    This method creates the command for adding a new user to the database

    :param connection: the database connection
    :return: the MySQL command to add new user
    """

    if __location is not None:
        db_add_location = query_strings.add_location.format(__street, __city, __state, __zip,
                                                            __country, __latitude, __longitude)

        db_get_location = query_strings.search_location.format(__street, __city, __state, __zip,
                                                               __country, __latitude, __longitude)

        with connection.cursor() as cur:
            cur.execute(db_get_location)
            location = cur.fetchone()
            # check if location already exists (to prevent duplicate entry)
            if location is None:  # if location DNE, create new location
                cur.execute(db_add_location)
                connection.commit()
                # get the ID of the newly created location
                cur.execute(db_get_location)
                location_id = cur.fetchone()[0]
            else:
                location_id = location[0]  # get the ID of the existing location

        db_add_user = query_strings.add_user.format(__display_name, __profile_pic, __email,
                                                    __first_name, __last_name, __mission_curator,
                                                    __birthday, location_id)
    else:  # add without any location
        db_add_user = query_strings.add_user_wo_location.format(__display_name, __profile_pic, __email,
                                                                __first_name, __last_name, __mission_curator,
                                                                __birthday)
    return db_add_user


def set_variables(request):
    """
    This method is used to set the variables for database entry

    :param request: The request_body dictionary object
    :return: nothing
    """

    global __first_name, __last_name, __display_name, __email, \
        __profile_pic, __mission_curator, __birthday, __location
    # checking for required fields
    try:
        __first_name = request['first_name']
        __last_name = request['last_name']
        __display_name = request['display_name']
        __email = request['email']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s)')

    # checking for optional fields
    try:
        __profile_pic = request['profile_pic']
    except KeyError:
        __profile_pic = ""

    try:
        __mission_curator = request['mission_curator']
    except KeyError:
        __mission_curator = 0  # false

    try:
        __birthday = request['birthday']
    except KeyError:
        __birthday = ""

    try:
        __location = request['location']
        set_location_variables()
    except KeyError:
        __location = None


def set_location_variables():
    """
    This method is used to set the location variables for database entry

    :return: nothing
    """

    global __street, __city, __state, __zip, __country, __latitude, __longitude
    try:
        __street = __location['street']
        __city = __location['city']
        __state = __location['state']
        __zip = __location['zip']
        __country = __location['country']
    except KeyError:
        raise HTTP_400_Exception('Missing required field(s) for Location')

    try:
        __latitude = __location['latitude']
    except KeyError:
        __latitude = 0

    try:
        __longitude = __location['longitude']
    except KeyError:
        __longitude = 0
