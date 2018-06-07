from response_objects.response_body import Body
from database_queries import *
from exceptions import *


# NOTE: this function must return a dictionary type
def get(request, query_str_param, connection):
    if query_str_param is None:
        query_str_param = {}
    try:
        email = query_str_param['email']
    except KeyError:
        raise HTTP_400_Exception('Missing required field - email')

    # query for user in the database
    user_query = query_strings.search_all_user_details_by_email.format(email)

    body = Body()
    with connection.cursor() as cur:
        cur.execute(user_query)
        item = cur.fetchone()

        # add user details
        if item is not None:
            body.addParameter('display_name', item[1])
            body.addParameter('profile_pic', item[2])
            body.addParameter('email', item[3])
            body.addParameter('first_name', item[4])
            body.addParameter('last_name', item[5])
            body.addParameter('mission_curator', False if item[6] == 0 else True)
            body.addParameter('birthday', item[7])

            # add user's address as location
            if item[8] is not None:

                # query for location using the location id
                cur.execute(query_strings.search_all_fields_location.format(item[8]))
                loc = cur.fetchone()
                location = dict()
                location['street'] = loc[1]
                location['city'] = loc[2]
                location['state'] = loc[3]
                location['zip'] = loc[4]
                location['country'] = loc[5]
                location['latitude'] = loc[6]
                location['longitude'] = loc[7]
                body.addParameter('location', location)
            else:
                body.addParameter('location', None)

    return body
