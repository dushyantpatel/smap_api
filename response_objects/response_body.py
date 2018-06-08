"""
This class will automatically genetate a body (str) to put
in your response object.
Call the addParameter() method to add key - value pairs in 
the body
"""


class Body:
    # initialize all local variables
    def __init__(self, body=None):
        self.__body = body

    # function to add a parameter to the body
    # NOTE: key must be of type string (str)
    def addParameter(self, key, value):
        if isinstance(key, str):
            if self.__body is None:
                self.__body = {}
            self.__body[key] = value
        else:
            raise Exception("In body, key must be of type str")

    # function to set the body
    # NOTE: the body must be of type dict
    def setBody(self, body):
        if isinstance(body, dict):
            self.__body = body
        elif body is not None:
            raise Exception("The body must be of type dict")

    # function to get the body
    def getBody(self):
        if self.__body is None or len(self.__body) == 0:
            return None
        return self.__body
