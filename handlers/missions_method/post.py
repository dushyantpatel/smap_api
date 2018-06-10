from response_objects.response_body import Body
from database_queries import *
from exceptions import *

requiredKeys = ['name', 'location', 'mission_start', 'mission_end', 'points', 'image','description', 'mission_date']
__street = ''
__city = ''
__state = ''
__zip = 0
__country = ''
__latitude = 0
__longitude = 0

# NOTE: this function must return a dictionary type
def post(request, query_str_param, connection):

    missions = request['missions']

    for mission in missions:
        verify_location(mission)

    for mission in missions:
        checkRequiredKeys(mission)
        check_require_loc_key(mission['location'])
        search_location = query_strings.search_for_location.format(__street, __city, __zip)
        add_location = query_strings.add_location.format(__street, __city, __state, __zip, __country,
                                                            __latitude, __longitude)
        locatoion_id = get_loc_id(add_location,search_location,connection )
        print(type(mission))
        command_add_mission = query_strings.add_mission_required_with_loc_id.format(mission['name'],locatoion_id, mission['mission_date'], mission['mission_start'],
                                                                        mission['mission_end'],
                                                                        mission['points'],
                                                                        mission['description'],
                                                                        mission['image'])

        with connection.cursor() as cur:
            cur.execute(command_add_mission)
            connection.commit()


    body = Body()
    body.addParameter('message', 'missions.post has been called')
    return body


def check_require_loc_key(mission):
    global __state, __country, __latitude, __longitude, __zip, __street, __city
    __street = mission['street']
    __state = mission['state']
    __city = mission['city'].lower()
    __longitude = mission['longitude']
    __zip = mission['zip']
    __latitude = mission['latitude']
    __country = mission['country']


def checkRequiredKeys(mission):
    missing_keys = []
    error = False
    for key in requiredKeys:
        try:
            value = mission[key]
        except KeyError:
            error = True
            missing_keys.append(key)

    if error:
        raise HTTP_400_Exception("Missing field [" + str(missing_keys) + "] which is a required field")
def set_varaibles(request):
    return


def verify_location(mission):
    # Checking required variables within location of events
    location = mission['location']
    required_fields = ['street', 'city', 'state', 'zip', 'country', 'latitude', 'longitude']
    for field in required_fields:
        if field not in location:
            raise HTTP_400_Exception('Missing required field - ' + field + ' in location for event - ' + str(mission))


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