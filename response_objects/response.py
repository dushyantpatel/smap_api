"""
This class will help you generate a response object (dict).
All you have to do is set the values.
In order to generate the response, call the getResponse() method.
"""


class Response:
    # initialize all local variables
    def __init__(self, statusCode=200, headers=None, body=None, isBase64Encoded=False):
        self.__statusCode = statusCode
        self.__headers = headers
        self.__body = body
        self.__isBase64Encoded = isBase64Encoded

    # function to set status code in the response
    # NOTE: statusCode must be of type int
    def setStatusCode(self, statusCode):
        if isinstance(statusCode, int):
            self.__statusCode = statusCode

    # function to set the headers in the response
    # NOTE: headers must be of type dice
    def setHeaders(self, headers):
        if isinstance(headers, dict):
            self.__headers = headers

    # function to set the body in the response
    def setBody(self, body):
        if isinstance(body, str):
            self.__body = body
        else:
            self.__body = str(body)

    # function to set the isBase64Encoded in the response
    # NOTE: isBase64Encoded must be of type bool
    def setIsBase64Encoded(self, isBase64Encoded):
        if isinstance(isBase64Encoded, bool):
            self.__isBase64Encoded = isBase64Encoded

    # function to generate the response object
    def getResponse(self):
        resp = {
            "isBase64Encoded": self.__isBase64Encoded,
            "statusCode": self.__statusCode,
            "headers": self.__headers,
            "body": self.__body
        }
        return resp
