import unittest
import ast
import pymysql
import rds_config
import sys
from tests.event import Event
from gateway import main_handler

# rds settings
rds_host = rds_config.db_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
connection = None

# resource settings
path = 'users'
context = None

class TestUsers(unittest.TestCase):
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
            cur.execute('SELECT * FROM user WHERE email="test.email@smap.com"')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM user WHERE user_id=' + str(row[0]))
            connection.commit()

    def test_add_new_event(self):
        self.req_body['name'] =  'Best Event'
        self.req_body['logo_url'] = "https://smap.com"
        self.req_body['category'] = 'Music'
        self.req_body['is_public'] = True
        self.req_body['event_data'] = '2018-06-15'
        self.req_body['start_time'] = '15:30:00'
        self.req_body['end_time'] = '20:30:00'
        self.req_body['points'] = '9000'
        self.req_body['event_url'] = "https://whatsamattau.com"
        self.req_body['street'] = 'Lame St.'
        self.req_body['state'] = 'CA'
        self.req_body['country'] = 'United States'
        self.req_body['zip'] = '92036'
        self.req_body['latitude'] = '36.7894'
        self.req_body['longitude'] = '420.786'
        self.req_body['location'] = {"street": self.req_body['street'], "state": self.req_body['state'], \
                                     "country": self.req_body['country'], "zip": self.req_body['zip'], \
                                     'latitude':self.req_body['latitude'], 'longitude': self.req_body['location']}
        self.req_body['popularity'] = 9000
        self.event.setBody(str(self.req_body))
        response = main_handler(self.event.getEvent(), context)
        resp_body = response['body']
        status_code = response['statusCode']

        # check for correct status code
        self.assertEqual(201, status_code)

        # check for correct body
        self.assertEqual(resp_body, str(None))


