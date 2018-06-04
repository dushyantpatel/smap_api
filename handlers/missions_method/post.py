# TODO - implementation

from response_objects.response_body import Body
from database_queries import *
from exceptions import *

requiredKeys = ['name', 'location', 'mission_date', 'mission_start', 'mission_end', 'points']

# NOTE: this function must return a dictionary type
def post(request, connection):

    missions = request['missions']
    for mission in missions:
        checkRequiredKeys(mission)
        built_location = query_strings.search_for_location(mission['location']['street'], mission['location']['city'], mission['location']['zip'])
        command_add_mission = query_strings.add_mission_required.format(mission['name'], built_location, mission['mission_date'], mission['mission_start'],
                                                                        mission['mission_end'], mission['points'])

        with connection.cursor() as cur:
            cur.execute(command_add_mission)
            connection.commit()


    body = Body()
    body.addParameter('message', 'missions.post has been called')
    return body

def checkRequiredKeys(mission):
    for key in requiredKeys:
        try:
            value = mission[key]
        except KeyError:
            raise HTTP_204_Exception("Missing field [" + key + "] which is a required field")


def set_varaibles(request):
    return



