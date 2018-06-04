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

    # for every event, fill in the missing optional fields and check for required fields
    for event in events:
        verify_event(event)  # this sets the temporary fields in events

    for event in events:

        # set all location variables in this event to the global location variables
        set_loc_vars(event)

        # using the query strings to search for location and adding location if it doesn't exist
        command_get_loc = query_strings.search_for_location.format(__street, __city, __zip)

        # using the query string to add location  if it wasn't found.
        command_add_loc = query_strings.add_location.format(__street, __city, __state, __zip, __country, __latitude,
                                                            __longitude)

        # Check Get_Loc first to see if id is already there so we don't duplicate ids
        location_id = get_loc_id(command_add_loc, command_get_loc, connection)

        # post the edited information of the event onto the data_base
        command_add_event = query_strings.add_event_required.format(event['name'], event['type'], str(location_id),
                                                                    event['event_date'], event['event_start'],
                                                                    event['event_end'], event['is_public'],
                                                                    event['is_free'])
        with connection.cursor() as cur:
            cur.execute(command_add_event)
            connection.commit()

    body = Body()
    body.addParameter('message', 'events.post has been called')
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
            print(location_id)
        else:
            # else just get already existing location_id
            location_id = cur.fetchone()[0]
    return location_id


def verify_event(event):

    # check for required fields
    required_fields = ['name', 'is_public', 'event_date', 'start_time', 'end_time', 'points', 'location']
    for field in required_fields:
        if field not in event:
            raise HTTP_400_Exception('Missing the field ' + field + ' in event: ' + str(event))

    # check for required fields in location
    verify_location(event['location'])

    # check if optional variables are there if not make them empty strings
    optional_fields = ['description', 'host']
    for field in optional_fields:
        if field not in event:
            event[field] = ''


def set_loc_vars(event):
    # set location variables in an event
    global __state, __country, __latitude, __longitude, __zip, __street, __city
    __state = event['location']['state']
    __country = event['location']['country']
    __latitude = event['location']['latitude']
    __longitude = event['location']['longitude']
    __zip = event['location']['zip']
    __street = event['location']['street']
    __city = event['location']['city']


def verify_location(location):
    required_fields = ['street', 'state', 'city', 'longitude', 'zip', 'latitude', 'country']
    for field in required_fields:
        if field not in location:
            raise HTTP_400_Exception('Missing the field ' + field + ' in location')
