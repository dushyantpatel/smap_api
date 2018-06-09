from response_objects.response_body import Body
from database_queries import *
from exceptions import *

__street = ''
__city = ''
__state = ''
__zip = ''
__country = ''
__latitude = ''
__longitude = ''


# NOTE: this function must return a dictionary type
def post(request, query_str_param, connection):
    if query_str_param is None:
        query_str_param = {}

    events = request['events']

    # verify all events first
    for event in events:
        verify_events(event)

    for event in events:

        # set global location variables to current location for convenience
        set_location_variables(event['location'])

        # using the query strings to search for location and adding location if it doesn't exist
        command_get_loc = query_strings.search_for_location.format(__street, __city, __zip)

        # using the query string to add location if it wasn't found.
        command_add_loc = query_strings.add_location.format(__street, __city, __state, __zip, __country,
                                                            __latitude, __longitude)

        # Check Get_Loc first to see if id is already there so we don't duplicate ids
        location_id = get_loc_id(command_add_loc, command_get_loc, connection)

        # Check if event is not already in the Data Base
        command_search_event = query_strings.search_for_event_in_db.format(event['name'], location_id)
        new_event = verify_new_event(command_search_event, connection)

        if new_event is False:
            continue
        # post the edited information of the event onto the data_base
        command_add_event = query_strings.add_event_all_fields_except_host.format(event['name'], event['type'],
                                                                                  location_id,
                                                                                  event['event_date'],
                                                                                  event['start_time'],
                                                                                  event['end_time'], event['is_public'],
                                                                                  event['is_free'], event['points'],
                                                                                  event['image'],
                                                                                  event['description'])
        with connection.cursor() as cur:
            cur.execute(command_add_event)
            connection.commit()

    body = Body()
    return body


def get_loc_id(command_add_loc, command_get_loc, connection):
    # checking if location_id is already within the data_base
    with connection.cursor() as cur:
        cur.execute(command_get_loc)
        location_id = cur.fetchone()

        if location_id is None:
            # if not push the new location information on the database to generate a location_id
            cur.execute(command_add_loc)
            connection.commit()
            cur.execute(command_get_loc)
            location_id = cur.fetchone()[0]
        else:
            # else just get already existing location_id
            location_id = location_id[0]
    return location_id


def verify_events(event):
    # checking if required variables are correct
    required_fields = ['name', 'type', 'location', 'event_date', 'start_time',
                       'end_time', 'is_public', 'is_free', 'points']
    required_fields_type = [str, str, dict, str, str, str, bool, bool, int]
    for field, field_type in zip(required_fields, required_fields_type):
        try:
            if type(event[field]) != field_type:
                raise HTTP_400_Exception('Expecting type ' +
                                         str(field_type) + ' for ' + field + ' in event: ' + str(event))
        except KeyError:
            raise HTTP_400_Exception('Missing required field - ' + field + ' in event: ' + str(event))

    # verify the location fields
    verify_location(event)

    # checking if optional fields exist
    optional_fields = ['description', 'host', 'image']
    for field in optional_fields:
        if field not in event:
            event[field] = ''
        else:
            if type(event[field]) != str:
                raise HTTP_400_Exception('Expecting ' + str(str) + ' for field ' + field + ' in event ' + str(event))


def verify_new_event(command_search_event, connection):
    # Checking if event is already in the DB by name and location
    with connection.cursor() as cur:
        cur.execute(command_search_event)
        found = cur.fetchone()
        return found is None


def verify_location(event):
    # Checking required variables within location of events
    location = event['location']
    required_fields = ['street', 'city', 'state', 'zip', 'country', 'latitude', 'longitude']
    required_fields_type = [str, str, str, int, str, float, float]
    for field, field_type in zip(required_fields, required_fields_type):
        try:
            if type(location[field]) != field_type:
                raise HTTP_400_Exception('Expecting type ' + str(field_type) +
                                         ' for "' + field + '" in location for event - ' + str(event))
        except KeyError:
            raise HTTP_400_Exception('Missing required field - ', field, ' in location for event - ', event)


def set_location_variables(location):
    # setting location global variables
    global __state, __country, __latitude, __longitude, __zip, __street, __city
    __street = location['street']
    __state = location['state']
    __city = location['city'].lower()
    __longitude = location['longitude']
    __zip = location['zip']
    __latitude = location['latitude']
    __country = location['country']
