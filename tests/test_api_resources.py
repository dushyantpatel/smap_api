import unittest
import ast
from tests.event import Event
from gateway import main_handler


context = ''  # sample context to pass to the api
methods = ['GET', 'POST', 'PUT', 'DELETE', 'OTHER']  # list of all possible methods
resources = ['mai', 'events', 'missions', 'plan', 'users', 'friends' 'other']  # list of all possible resources
message_template = '{0}.{1} has been called'  # sample message template to check for in response body

# This list is parallel to the resources list.
# It will tell us how many methods to check. Ex. first 4 methods
num_valid_methods = [1, 4, 4, 4, 3, 3, 0]


class TestAPIResources(unittest.TestCase):

    def setUp(self):
        self.event = Event()

    def run_tests(self, id):
        self.resource = resources[id]
        self.num_methods = num_valid_methods[id]
        self.event.setPath(self.resource)
        # event = Event()

        # test all valid methods
        for method in methods[:self.num_methods]:
            self.event.setHttpMethod(method)
            msg = message_template.format(self.resource, method.lower())
            res = main_handler(self.event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[self.num_methods:]:
            self.event.setHttpMethod(method)
            res = main_handler(self.event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))

    # def test_mai(self):
    #     self.run_tests(0)
    #
    # def test_events(self):
    #     self.run_tests(1)
    #
    # def test_missions(self):
    #     self.run_tests(2)
    #
    # def test_plan(self):
    #     self.run_tests(3)
    #
    # def test_users(self):
    #     self.run_tests(4)
    #
    # def test_friends(self):
    #     self.run_tests(5)


if __name__ == '__main__':
    unittest.main()