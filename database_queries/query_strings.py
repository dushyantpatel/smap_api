"""
This file has all the query string templates for the MySQL database.
"""
# -------------------------------------------------------------------------------
# Locations
# -------------------------------------------------------------------------------
# add a brand new location with all information
add_location = 'INSERT INTO location (street, city, state, zip, country, latitude, longitude) ' \
               'VALUES ("{0}", "{1}", "{2}", {3}, "{4}", {5}, {6});'

# search all locations
search_all_locations = 'SELECT * FROM location;'

# search specific location knowing the street, city, and zip
search_for_location = 'SELECT location_id FROM location WHERE street="{0}" AND city="{1}" AND zip={2};'

# -------------------------------------------------------------------------------
# Users
# -------------------------------------------------------------------------------
# add a brand new user with all information
add_user = 'INSERT INTO user (display_name, profile_pic, email, first_name, last_name, missionCurator, ' \
           'birthday, location) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", {5}, "{6}", {7});'

# add a brand new user without the their location
add_user_wo_location = 'INSERT INTO user (display_name, profile_pic, email, first_name, last_name, ' \
                       'missionCurator, birthday) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", {5}, "{6}");'

# add a brand new user with only required fields
add_user_required = 'INSERT INTO user (display_name, email, first_name, last_name, missionCurator) ' \
                    'VALUES ("{0}", "{1}", "{2}", "{3}", {4});'

# search all users
search_all_users = 'SELECT * FROM user;'

# search specific user knowing their email
search_for_user_email = 'SELECT user_id FROM user WHERE email="{0}";'

# search specific user knowing their email
search_for_user_display_name = 'SELECT user_id FROM user WHERE display_name="{0}";'

# -------------------------------------------------------------------------------
# Friends List
# -------------------------------------------------------------------------------
# friend request sent from a specific user
friend_requested = 'INSERT INTO friendsList (user1, user2, is_friend) VALUES (' \
                   + search_for_user_email + ',' + search_for_user_email + ', "{2}");'

# link two friends when user accepts friend request
friend_request_accepted = 'UPDATE friendsList SET is_friend="{0}" WHERE user1=' + search_for_user_email + ' ; ' \
                          'INSERT INTO friendsList (user1, user2, is_friend) VALUES (' \
                          + search_for_user_email + ',' + search_for_user_email + ', "{5}");'

# delete from the table if friend request is rejected
friend_request_rejected = 'DELETE FROM friendsList WHERE user1=' + search_for_user_email + ' ' \
                          'AND user2=' + search_for_user_email + ';'

# search friends list of a specific user
search_friends = 'SELECT user2 FROM friendsList WHERE user1=' + search_for_user_email + ' AND is_friend="{1}";'

# search all pending friend requests of a specific user
search_pending_requests = 'SELECT user1 FROM friendsList WHERE user2=' + search_for_user_email + ' AND is_friend="{1}";'

# search all friend requests a user has sent
search_requests_sent = 'SELECT user2 FROM friendsList WHERE user1=' + search_for_user_email + ' AND is_friend="{1}";'

# -------------------------------------------------------------------------------
# Events
# -------------------------------------------------------------------------------
# add a brand new event with all information
add_event = 'INSERT INTO event (name, image, type, host, description, location, event_date,' \
            ' event_start, event_end, is_public, is_free, points) VALUES ("{0}", "{1}", "{2}", ' \
            + search_for_user_email + ', "{6}",' + search_for_location + ', "{10}", "{11}", "{12}", {13}, {14}, {15});'

# add a brand new event with only required fields and knowing the address
add_event_required = 'INSERT INTO event (name, type, location, event_date, event_start, event_end, ' \
                     'is_public, is_free, points) VALUES ("{0}", "{1}",' + search_for_location \
                     + ', "{5}", "{6}", "{7}", {8}, {9}, {10});'

# search all events
search_all_events = 'SELECT event_id FROM event;'


# search specific event knowing the event city
search_for_event_city = 'SELECT event_id FROM event WHERE city="{0}";'

# search specific event knowing the event type
search_for_event_type = 'SELECT event_id FROM event WHERE type="{0}";'

# -------------------------------------------------------------------------------
# Event Linking Table
# -------------------------------------------------------------------------------
# link specific event to specific user
link_event_history = 'INSERT INTO eventHistory (is_going, user, event) VALUES ("{0}",' \
                     + search_for_user_email + ',' + search_for_event_city + ');'

# -------------------------------------------------------------------------------
# Missions
# -------------------------------------------------------------------------------
# add a brand new mission with all information
add_mission = 'INSERT INTO mission (name, image, description, location, mission_date, mission_start, ' \
              'mission_end, points) VALUES ("{0}", "{1}", "{2}",' + search_for_location + \
              ', "{6}", "{7}", "{8}", {9});'

# add a brand new mission with only required fields
add_mission_required = 'INSERT INTO mission (name, location, mission_date, mission_start, mission_end, points)' \
                       ' VALUES ("{0}",' + search_for_location + ', "{4}", "{5}", "{6}", {7});'

# search all missions
search_all_missions = 'SELECT * FROM mission;'

# search specific mission knowing the mission name
search_for_mission = 'SELECT mission_id FROM mission WHERE name="{0}"'

# -------------------------------------------------------------------------------
# Mission Linking Table
# -------------------------------------------------------------------------------
# link specific mission to specific user
link_mission_history = 'INSERT INTO missionHistory (is_going, user, mission) VALUES ("{0}",' \
                       + search_for_user_email + ',' + search_for_mission + ');'
