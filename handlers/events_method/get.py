from response_objects.response_body import Body
from database_queries import *
from exceptions import *


# NOTE: this function must return a dictionary type
def get(request, query_str_param, connection):
    body = Body()

    # return all events if query_str_param is None
    if query_str_param is None:
        body.setBody(get_events(connection))
        return body

    if 'city' in query_str_param:
        city = query_str_param['city']
        city = city.lower()
        body.setBody(get_events(connection, city))
        return body

    if 'event_id' in query_str_param:
        event_id = query_str_param['event_id']
        event = get_events(connection, None, event_id)
        if len(event) == 0:
            return body
        else:
            body.setBody(event[0])
            return body

    raise HTTP_400_Exception('Missing required fields for get events')


def get_events(connection, city=None, event_id=None):
    events = list()
    with connection.cursor() as cur:
        if city is None and event_id is None:
            cur.execute(query_strings.get_all_events)
        elif city is not None:
            cur.execute(query_strings.search_for_all_event_fields_city.format(city))
        else:
            cur.execute(query_strings.search_event_by_id.format(event_id))
        li = cur.fetchall()
    for item in li:
        event = dict()
        event['event_id'] = item[0]
        event['name'] = item[1]
        event['image'] = item[2]
        event['type'] = item[3]
        host_id = item[4]
        if host_id is not None:
            with connection.cursor() as cur:
                cur.execute(query_strings.search_user_email_by_user_id.format(host_id))
                event['host'] = cur.fetchone()[0]
        else:
            event['host'] = None
        event['description'] = item[5]
        location_id = item[6]
        if location_id is not None:
            with connection.cursor() as cur:
                cur.execute(query_strings.search_all_fields_location.format(location_id))
                loc = cur.fetchone()
            location = dict()
            location['street'] = loc[1]
            location['city'] = loc[2].title()
            location['state'] = loc[3]
            location['zip'] = loc[4]
            location['country'] = loc[5]
            location['latitude'] = loc[6]
            location['longitude'] = loc[7]
            event['location'] = location
        else:
            event['location'] = None
        event['event_date'] = item[7]
        event['start_time'] = item[8]
        event['end_time'] = item[10]
        event['is_public'] = item[11]
        event['is_free'] = item[12]
        event['points'] = item[13]
        events.append(event)

    return events
