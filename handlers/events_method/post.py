# TODO - implementation
from response_objects.response_body import Body
import pymysql
from database_queries import *

# NOTE: this function must return a dictionary type
def post(request, connection):
    connection = pymysql.connect()
    events = request['Events']

    #{0}: Event name, {1}: Logo_URL, {2}:Type,
    #{3}: Eventsbrite_URL, {4}:Description
    #{5}: event_data, {6}: event_start, {7}: event_end
    #{8}: is_public, {9}:free_event, #{10}:points
    #{11}: location

    #{0}: location:street, {1}:location:city,
    #{2}:location:region, {3}location:postal_code,
    #{4}:location:country, {5}:location:latitude,
    #{6}:location:longitude

    db_String_Loc = query_strings.add_location
    db_String = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}"
    for event in events:
        command_Loc = db_String_Loc.format( event['location']['street'], event['location']['city'],
                                   event['location']['region'], event['location']['postal_code'],
                                   event['location']['country'], event['location']['latitude'],
                                   event['location']['longitude'])

        with connection.cursor() as cur:
            cur.execute(command_Loc)
            connection.commit()
            cur.execute()
            cur.fetchone()

        command = db_String.format(event['name'],event['logo_url'], event['category'], event['description'],
                                   event['event_data'], event['start_time'], event['end_time'],
                                   event['is_public'], event['free_event'], event['points'])

        with connection.cursor() as cur:
            cur.execute(command)
            connection.commit()


    body = Body()
    body.addParameter('message', 'events.post has been called')
    return body
