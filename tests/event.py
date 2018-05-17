import tests.sample_event as sample_event

"""
This class will be used to create test events for the smap-api

Key things to be noted:
path                    - must be of type (str)
httpMethod              - must be of type (str)
queryStringParameters   - must be of type (dict)
body                    - must be of type str( dict )
"""


class Event:

    def __init__(self, path='', httpMethod=None, queryStringParameters=None, body=None):
        # initialize event variable
        self.__event = sample_event.event
        self.setPath(path)
        self.setHttpMethod(httpMethod)
        self.setQueryStringParameters(queryStringParameters)
        self.setBody(body)

    def setPath(self, path):
        # set all path variables in event
        self.__event['path'] = '/' + path
        self.__event['requestContext']['path'] = '/testDeployment_1/' + path
        self.__event['pathParameters'] = {'proxy': path}

    def setHttpMethod(self, httpMethod):
        # set all httpMethod variables in event
        self.__event['httpMethod'] = httpMethod
        self.__event['requestContext']['httpMethod'] = httpMethod

    def setQueryStringParameters(self, queryStringParameters):
        # set queryStringParameters in event
        self.__event['queryStringParameters'] = queryStringParameters

    def setBody(self, body):
        # set body in event
        self.__event['body'] = body

    def getEvent(self):
        # return the event object (dict)
        return self.__event
