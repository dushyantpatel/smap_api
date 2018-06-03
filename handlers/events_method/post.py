# TODO - implementation
from response_objects.response_body import Body
from database_queries import *
from exceptions import *

__name = ''
__event_url = ''
__category = ''
__description = ''
__event_date = ''
__start_time = ''
__image = ''
__end_time = ''
__points = ''
__is_public = ''
__street = ''
__is_free = 0
__city = ''
__state = ''
__zip = ''
__country = ''
__latitude = ''
__longitude = ''
__location = None
__popularity = 0


# NOTE: this function must return a dictionary type
def post(request, connection):
    events = request['events']
    real_Events = {}
    real_Events["edited"] = []


    #{0}:location:street, {1}:location:city,
    #{2}:location:region, {3}location:postal_code,
    #{4}:location:country, {5}:location:latitude,
    #{6}:location:longitude


    #{0}: Event name, {1}: Logo_URL, {2}:Type,
    #{3}: Eventsbrite_URL, {4}:Description
    #{5}: event_data, {6}: event_start, {7}: event_end
    #{8}: is_public, {9}:free_event, #{10}:points
    #{11}: location

    for event in events:

        set_event_vars(event)
        real_Events['edited'].append({'name' : __name,'description' : __description, 'image': __image,
                                     'event_url' : __event_url, 'start_time' : __start_time,
                                     'end_time' : __end_time, 'free_event' : __is_free,
                                     'category' : __category, 'location': __location, 'points': __points,
                                     'is_public' : __is_public, 'event_data' : __event_date})


    for event in real_Events['edited']:

        set_edited_location(event['location'])

        # using the query strings to search for location and adding loction if it doesn't exist
        command_get_Loc = query_strings.search_location(__street, __city, __state, __zip, __country, __latitude, __longitude)



        # using the query string to add loction  if it wasn't found.
        command_add_loc = query_strings.add_location(__street, __city, __state, __zip, __country, __latitude, __longitude)

        #Check Get_Loc first to see if id is already tehre so we don't duplicate ids
        location_id = get_loc_id(command_add_loc, command_get_Loc, connection)

        #post the edited information of the event onto the data_base
        command_add_event = query_strings.add_event(__name, __event_url, __category, __description, __event_date,
                                                    __start_time, __end_time,__points,__popularity,location_id)
        with connection.cursor() as cur:
            cur.execute(command_add_event)
            connection.commit()


    body = Body()
    body.addParameter('message', 'events.post has been called')
    return body


def get_loc_id(command_add_loc, command_get_Loc, connection):
    #checking if location_id is already within the data_base
    with connection.cursor() as cur:
        cur.execute(command_get_Loc)
        location_id = cur.fetchone()

        if location_id is None:
            #if not push the new location infomation on the database to generate a location_id
            cur.execute(command_add_loc)
            connection.commit()
            cur.execute(command_add_loc)
            location_id = cur.fetchone()[0]
        else:
            #else just get already existing location_id
            location_id = cur.fetchone()[0]
    return location_id


def set_event_vars(event):
    global __name,  __event_url, __category, __is_public, __event_date, __is_free, \
     __start_time, __end_time, __points, __location, __description, __host, __image, __popularity

    #checking if required variables are correct
    try:
        __name = event['name']
        __image = event['logo_url']
        __category = event['category']
        __is_public = event['is_public']
        __event_date = event['event_data']
        __start_time = event['start_time']
        __end_time = event['end_time']
        __points = event['points']
        __event_url = event['event_url']
        __location = event['location']
        __popularity = event['popularity']
        set_loc_vars(event)
    #raise except if they're not that and terminate
    except KeyError:
        raise HTTP_204_Exception("Missing a required field")
    __location = {"street": __street, "state": __state, "country": __country,
                "zip": __zip, 'latitude': __latitude, 'longitude': __longitude,
                "city": __city}
    #check if optional variables are there if not make them empty strings
    try:
        __description = event['description']
    except KeyError:
        __description = ""
    try:
        __host = event['host']
    except KeyError:
        __host = ""



def set_loc_vars(event):
    # Checking required variables within location of events
    global __state,__country,__latitude,__longitude,__zip,__street,__city
    try:
        __state = event['location']['region']
        __country = event['location']['country']
        __latitude = event['location']['latitude']
        __longitude = event['location']['longitude']
    # exectoion case of required variables is not there
    except KeyError:
        raise HTTP_204_Exception("Missing a required field")
    # Checking optional variables within location of events
    # If not there set field to N/A
    # check zip
    try:
        __zip = event['location']['postal_code']
    except KeyError:
        __zip = ""
    # Check street address
    try:
        __street = event['location']['street']
    except KeyError:
        __street = ""
    # check city
    try:
        __city = event['location']['city']
    except KeyError:
        __city = ""



def set_edited_location(location):
    #setting edited location
    global __state,__country,__latitude,__longitude,__zip,__street,__city
    __street = location['street']
    __state = location['state']
    __city = location['city']
    __longitude = location['longitude']
    __zip = location['zip']
    __latitude = location['latitude']
    __country = location['country']

