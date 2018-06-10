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
path = 'missions'
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
            cur.execute('SELECT * FROM mission WHERE name="New Mission"')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM mission WHERE mission_id=' + str(row[0]))
            connection.commit()

            cur.execute('SELECT * FROM location WHERE latitude=0.000 AND longitude=0.000')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM location WHERE location_id=' + str(row[0]))
            connection.commit()

    def test_add_new_event(self):
        self.event.setHttpMethod('POST')
        test_dict = {'missions': []}
        mission_name = 'New Mission'
        mission_type = 'Adventure'
        mission_date = '2018-06-15'
        start_time = '15:30:00'
        end_time = '20:30:00'
        description = "Sucks to succk"
        image = ""
        points = 9000
        location = {"street": 'Lame St.', "state": 'CA', "city": 'san diego',
                    "country": 'United States', "zip": 92364,
                    "latitude": 0.000, "longitude": 0.000}

        test_dict['missions'].append({'name': mission_name, 'mission_start': start_time,
                                    'mission_end': end_time, 'description': description,
                                    'location': location, 'points': points,'mission_date': mission_date, 'image': image})
        self.req_body['missions'] = test_dict['missions']
        self.event.setBody(json.dumps(self.req_body))
        response = main_handler(self.event.getEvent(), context)
        resp_body = json.loads(response['body'])
        print(resp_body)
        status_code = response['statusCode']
        print(response)

        # check for correct status code
        self.assertEqual(201, status_code)

        # check for correct body
        self.assertEqual(None, resp_body)
