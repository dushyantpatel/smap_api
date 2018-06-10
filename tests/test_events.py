import unittest
import pymysql
import rds_config
import sys
import json
from tests.event import Event
from gateway import main_handler

# rds settings
rds_host = rds_config.db_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
connection = None

# resource settings
path = 'events'
context = None


class TestEvents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global connection
        # connect to database
        try:
            connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        except pymysql.err.Error as ex:
            template = "ERROR: {0} - Could not connect to MySql instance \n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit()

    @classmethod
    def tearDownClass(cls):
        connection.close()

    def setUp(self):
        self.event = Event()
        self.event.setPath(path)
        self.req_body = dict()

    def tearDown(self):
        # clean up the database
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM event WHERE name="Best Event"')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM event WHERE event_id=' + str(row[0]))
            connection.commit()

            cur.execute('SELECT * FROM location WHERE latitude=0.000 AND longitude=0.000')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM location WHERE location_id=' + str(row[0]))
            connection.commit()

    def test_add_new_event(self):
        self.event.setHttpMethod('POST')
        test_dict = {'events': []}
        event_name = 'Best Event'
        event_type = 'Music'
        is_public = True
        event_date = '2018-06-15'
        start_time = '15:30:00'
        end_time = '20:30:00'
        points = 9000
        is_free = False
        location = {"street": 'Lame St.', "state": 'CA', "city": 'San Diego',
                    "country": 'United States', "zip": 92364,
                    "latitude": 0.000, "longitude": 0.000}

        test_dict['events'].append({'name': event_name, 'start_time': start_time,
                                    'end_time': end_time, 'is_free': is_free,
                                    'location': location, 'points': points, 'is_public': is_public,
                                    'event_date': event_date, 'type': event_type})
        self.req_body['events'] = test_dict['events']
        self.event.setBody(json.dumps(self.req_body))
        response = main_handler(self.event.getEvent(), context)
        resp_body = json.loads(response['body'])
        status_code = response['statusCode']

        # check for correct status code
        self.assertEqual(201, status_code)

        # check for correct body
        self.assertEqual(None, resp_body)

    def test_get_event_by_id(self):
        self.event.setHttpMethod('GET')
        self.event.setQueryStringParameters({'event_id': "27"})
        response = main_handler(self.event.getEvent(), context)
        status_code = response['statusCode']

        # check for correct status code
        self.assertEqual(200, status_code)

    # def test_chriss_events(self):
    #     self.event.setHttpMethod('POST')
    #     with open('events.txt', 'r') as file:
    #         line = file.readline()
    #     self.event.setBody(line)
    #     # obj = dict(json.loads(line))
    #     # for item in obj['events']:
    #     #     print(item['image'])
    #
    #     response = main_handler(self.event.getEvent(), context)
    #     status_code = response['statusCode']
    #     headers = response['headers']
    #     print(headers['details'])
    #     print(status_code)
