import unittest
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
path = 'friends'
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

        # setup test users in the database
        add_usr_template = 'INSERT INTO user (display_name, email, first_name, last_name, missionCurator) ' \
                           'VALUES ("{0}", "{1}", "{2}", "{3}", {4});'
        add_usr1 = add_usr_template.format('test_user', 'test1.email@smap.com', 'Test1', 'Case1', 0)
        add_usr2 = add_usr_template.format('test_user', 'test2.email@smap.com', 'Test2', 'Case2', 0)
        add_usr3 = add_usr_template.format('test_user', 'test3.email@smap.com', 'Test3', 'Case3', 0)
        add_usr4 = add_usr_template.format('test_user', 'test4.email@smap.com', 'Test4', 'Case4', 0)
        with connection.cursor() as cur:
            cur.execute(add_usr1)
            cur.execute(add_usr2)
            cur.execute(add_usr3)
            cur.execute(add_usr4)
            connection.commit()

    @classmethod
    def tearDownClass(cls):
        # clean up the database
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM user WHERE display_name="test_user"')
            li = cur.fetchall()
            for row in li:
                cur.execute('DELETE FROM user WHERE user_id=' + str(row[0]))
            connection.commit()
        connection.close()

    def setUp(self):
        self.event = Event()
        self.event.setPath(path)
        self.req_body = dict()

    def tearDown(self):
        return

    def test_add_new_user(self):
        self.event.setHttpMethod('POST')

        # add user with required fields
        self.req_body['display_name'] = 'test_user'
        self.req_body['email'] = 'test.email@smap.com'
        self.req_body['first_name'] = 'Test'
        self.req_body['last_name'] = 'Case'
        self.event.setBody(str(self.req_body))

        response = main_handler(self.event.getEvent(), context)
        resp_body = response['body']
        status_code = response['statusCode']

        # check for correct status code
        self.assertEqual(201, status_code)

        # check for correct body
        self.assertEqual(resp_body, str(None))

