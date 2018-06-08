"""
This class will help you generate a header (dict) for your
response object.
Call the addParameter() method to add key - value pairs in 
the header
Then call the getHeader() method to get the header (dict)
"""


class Header:
    # initialize all local variables
    def __init__(self, header=None):
        self.__header = header

    # function to add a parameter to the header
    # NOTE: key must be of type string (str)
    def addParameter(self, key, value):
        if isinstance(key, str):
            if self.__header is None:
                self.__header = {}
            self.__header[key] = value
        else:
            raise Exception("In header, key must be of type str")

    # function to get the header as a dictionary
    def getHeader(self):
        return self.__header
