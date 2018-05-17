import unittest
import ast
from tests.event import Event
from gateway import main_handler


context = ''  # sample context to pass to the api
methods = ['GET', 'POST', 'PUT', 'DELETE', 'OTHER']  # list of all possible methods
resources = ['mai', 'events', 'missions', 'plan', 'users', 'other']  # list of all possible resources
message_template = '{0}.{1} has been called'  # sample message template to check for in response body

# This list is parallel to the resources list.
# It will tell us how many methods to check. Ex. first 4 methods
num_valid_methods = [1, 4, 4, 4, 3, 0]


class TestAPIResources(unittest.TestCase):

    def test_mai(self):
        resource = resources[0]
        num_methods = num_valid_methods[0]
        event = Event()
        event.setPath(resource)

        # test all valid methods
        for method in methods[:num_methods]:
            event.setHttpMethod(method)
            msg = message_template.format(resource, method.lower())
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[num_methods:]:
            event.setHttpMethod(method)
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))

    def test_events(self):
        resource = resources[1]
        num_methods = num_valid_methods[1]
        event = Event()
        event.setPath(resource)

        # test all valid methods
        for method in methods[:num_methods]:
            event.setHttpMethod(method)
            msg = message_template.format(resource, method.lower())
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[num_methods:]:
            event.setHttpMethod(method)
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))

    def test_missions(self):
        resource = resources[2]
        num_methods = num_valid_methods[2]
        event = Event()
        event.setPath(resource)

        # test all valid methods
        for method in methods[:num_methods]:
            event.setHttpMethod(method)
            msg = message_template.format(resource, method.lower())
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[num_methods:]:
            event.setHttpMethod(method)
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))

    def test_plan(self):
        resource = resources[3]
        num_methods = num_valid_methods[3]
        event = Event()
        event.setPath(resource)

        # test all valid methods
        for method in methods[:num_methods]:
            event.setHttpMethod(method)
            msg = message_template.format(resource, method.lower())
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[num_methods:]:
            event.setHttpMethod(method)
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))

    def test_users(self):
        resource = resources[4]
        num_methods = num_valid_methods[4]
        event = Event()
        event.setPath(resource)

        # test all valid methods
        for method in methods[:num_methods]:
            event.setHttpMethod(method)
            msg = message_template.format(resource, method.lower())
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 200)
            body = ast.literal_eval(res['body'])
            self.assertEqual(body['message'], msg)

        # test all invalid methods
        for method in methods[num_methods:]:
            event.setHttpMethod(method)
            res = main_handler(event.getEvent(), None)
            self.assertEqual(res['statusCode'], 501)
            self.assertEqual(res['body'], str(None))


if __name__ == '__main__':
    unittest.main()