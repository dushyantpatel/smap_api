"""
This file has all the query string templates for the MySQL database.
"""
# -------------------------------------------------------------------------------
# Locations
# -------------------------------------------------------------------------------
# add a brand new location with all information
add_location = 'INSERT INTO location (street, city, state, zip, country, latitude, longitude) ' \
               'VALUES ("{}", "{}", "{}", {}, "{}", {}, {});'

# search all locations
search_all_locations = 'SELECT location_id FROM location;'

# search all fields from location
search_all_fields_location = 'SELECT * FROM location WHERE location_id={}'

# search specific location knowing the street, city, and zip
search_for_location = 'SELECT location_id FROM location WHERE street="{}" AND city="{}" AND zip={};'

# -------------------------------------------------------------------------------
# Users
# -------------------------------------------------------------------------------
# add a brand new user with all information
add_user = 'INSERT INTO user (display_name, profile_pic, email, first_name, last_name, missionCurator, ' \
           'birthday, location) VALUES ("{}", "{}", "{}", "{}", "{}", {}, "{}", {});'

# add a brand new user without the their location
add_user_wo_location = 'INSERT INTO user (display_name, profile_pic, email, first_name, last_name, ' \
                       'missionCurator, birthday) VALUES ("{}", "{}", "{}", "{}", "{}", {}, "{}");'

# add a brand new user with only required fields
add_user_required = 'INSERT INTO user (display_name, email, first_name, last_name, missionCurator) ' \
                    'VALUES ("{}", "{}", "{}", "{}", {});'

# search all users
search_all_users = 'SELECT user_id FROM user;'

# search all user details by email
search_all_user_details_by_email = 'SELECT * FROM user WHERE email="{}"'

# search for user email by user_id
search_user_email_by_user_id = 'SELECT email FROM user WHERE user_id={}'

# search specific user knowing their email
search_for_user_email = 'SELECT user_id FROM user WHERE email="{}";'

# search specific user knowing their email
search_for_user_display_name = 'SELECT user_id FROM user WHERE display_name="{}";'

# update the user's display name
update_display_name = 'UPDATE user SET display_name="{}" WHERE email="{}";'

# update the user's profile pic
update_profile_pic = 'UPDATE user SET profile_pic="{}" WHERE email="{}";'

# update the user's email
update_email = 'UPDATE user SET email="{}" WHERE email="{}";'

# update the user's birthday
update_birthday = 'UPDATE user SET birthday="{}" WHERE email="{}";'

# update the user's location
update_location = 'UPDATE user SET location=' + '(' + search_for_location + ')' + ' WHERE email="{}";'

# -------------------------------------------------------------------------------
# Friends List
# -------------------------------------------------------------------------------
# friend request sent from a specific user
# user1 has requested user2 to be a friend
friend_requested = 'INSERT INTO friendsList (user1, user2, is_friend) VALUES (' \
                   + '(' + search_for_user_email + '), (' + search_for_user_email + '), "{}");'

# link two friends when user accepts friend request
# update user1 --> user2 to be a friend
# add a new row for user2 --> user1
friend_request_accepted = 'UPDATE friendsList SET is_friend="yes" WHERE user1=' + '(' + search_for_user_email + ') ' \
                          'AND user2=' + '(' + search_for_user_email + ');' \
                          'INSERT INTO friendsList (user1, user2, is_friend) VALUES ((' \
                          + search_for_user_email + '),(' + search_for_user_email + '), "yes");'

# delete from the table if friend request is rejected
friend_request_rejected = 'DELETE FROM friendsList WHERE user1=' + '(' + search_for_user_email + ') ' \
                          'AND user2=' + search_for_user_email + ';'

# search friends list of a specific user
search_friends = 'SELECT user2 FROM friendsList WHERE user1=' + '(' + search_for_user_email + ')' \
                 + ' AND is_friend="yes";'

# search all pending friend requests of a specific user
search_pending_requests = 'SELECT user1 FROM friendsList WHERE user2=' + '(' + search_for_user_email + ') ' \
                          'AND is_friend="NULL";'

# search all friend requests a user has sent
search_requests_sent = 'SELECT user2 FROM friendsList WHERE user1=' + '(' + search_for_user_email + ') ' \
                       'AND is_friend="NULL";'

# -------------------------------------------------------------------------------
# Events
# -------------------------------------------------------------------------------
# add a brand new event with all information
add_event = 'INSERT INTO event (name, image, type, host, description, location, event_date,' \
            ' event_start, event_end, is_public, is_free, points) VALUES ("{}", "{}", "{}", ' \
            + '(' + search_for_user_email + '), "{}", {}, ' \
            '"{}", "{}", "{}", {}, {}, {});'

# add a brand new event with only required fields and knowing the address
add_event_required = 'INSERT INTO event (name, type, location, event_date, event_start, event_end, ' \
                     'is_public, is_free, points) VALUES ("{}", "{}", {}, "{}", "{}", "{}", {}, {}, {});'

# add event with all fields except the host
add_event_all_fields_except_host = 'INSERT INTO event (name, type, location, event_date, event_start, event_end, ' \
                     'is_public, is_free, points, image, description) VALUES' \
                                   ' ("{}", "{}", {}, "{}", "{}", "{}", {}, {}, {}, "{}", "{}");'

# search all events
search_all_events = 'SELECT event_id FROM event;'

# get all events
get_all_events = 'SELECT * FROM event'

# search specific event knowing the event city
search_for_event_city = 'SELECT event_id FROM event WHERE city="{}";'

# search specific event knowing the event city
search_for_all_event_fields_city = 'SELECT * FROM event WHERE city="{}";'

# search event by id
search_event_by_id = 'SELECT * FROM event WHERE event_id={}'

# search if event exists in database
search_for_event_in_db = 'SELECT event_id FROM event WHERE name="{}" AND location={}'

# search specific event knowing the event type
search_for_event_type = 'SELECT event_id FROM event WHERE type="{}";'

# find the count of each response for an event
count_event_responses = 'SELECT (' + search_for_event_city + '), COUNT(*) FROM eventHistory GROUP BY is_going;'

# -------------------------------------------------------------------------------
# Event Linking Table
# -------------------------------------------------------------------------------
# link specific event to specific user
link_event_history = 'INSERT INTO eventHistory (is_going, user, event) VALUES ("{}",' \
                     + '(' + search_for_user_email + '),' + '(' + search_for_event_city + '));'

# -------------------------------------------------------------------------------
# Missions
# -------------------------------------------------------------------------------
# add a brand new mission with all information
add_mission = 'INSERT INTO mission (name, image, description, location, mission_date, mission_start, ' \
              'mission_end, points, type,) VALUES ("{}", "{}", "{}",(' + search_for_location + \
              '), "{}", "{}", "{}", {}, "{}", "{}");'

# add a brand new mission with only required fields
add_mission_required = 'INSERT INTO mission (name, location, mission_date, mission_start, mission_end, points, description, image)' \
                       ' VALUES ("{}",(' + search_for_location + '), "{}", "{}", "{}", {}, "{}", "{}");'

# search all missions
search_all_missions = 'SELECT mission_id FROM mission;'

# search specific mission knowing the mission name
search_for_mission = 'SELECT mission_id FROM mission WHERE name="{0}"'

# -------------------------------------------------------------------------------
# Mission Linking Table
# -------------------------------------------------------------------------------
# link specific mission to specific user
link_mission_history = 'INSERT INTO missionHistory (is_going, user, mission) VALUES ("{}",' \
                       + '(' + search_for_user_email + '),' + '(' + search_for_mission + '));'
