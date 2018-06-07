import unittest
import pymysql
import rds_config
import sys
from tests.event import Event
from gateway import main_handler
import json

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

    def test_add_new_user(self):
        self.event.setHttpMethod('POST')

        # add user with required fields
        self.req_body['display_name'] = 'test_user'
        self.req_body['email'] = 'test.email@smap.com'
        self.req_body['first_name'] = 'Test'
        self.req_body['last_name'] = 'Case'
        self.event.setBody(str(self.req_body))

        response = main_handler(self.event.getEvent(), context)

        resp_body = json.loads(response['body'])
        status_code = response['statusCode']

        # check for correct status code
        self.assertEqual(201, status_code)

        # check for correct body
        self.assertEqual(None, resp_body)

