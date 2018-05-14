"""
This class will automatically genetate a body (str) to put
in your response object.
Call the addParameter() method to add key - value pairs in 
the body
"""


class Body:
    # initialize all local variables
    def __init__(self):
        self.__body = {}

    # function to add a parameter to the body
    # NOTE: key must be of type string (str)
    def addParameter(self, key, value):
        if isinstance(key, str):
            self.__body[key] = value

    # function to set the body
    # NOTE: the body must be of type dict
    def setBody(self, body):
        if isinstance(body, dict):
            self.__body = body

    # function to get the string for body
    def getBody(self):
        return str(self.__body)

    # alternate way to get the string
    def __str__(self):
        return self.getBody()

    __repr__ = __str__
