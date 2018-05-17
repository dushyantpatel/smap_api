"""
This class will help you generate a header (dict) for your
response object.
Call the addParameter() method to add key - value pairs in 
the header
Then call the getHeader() method to get the header (dict)
"""


class Header:
    # initialize all local variables
    def __init__(self, header={}):
        self.__header = header

    # function to add a parameter to the header
    # NOTE: key must be of type string (str)
    def addParameter(self, key, value):
        if isinstance(key, str):
            self.__header[key] = value

    # function to get the header as a dictionary
    def getHeader(self):
        if not len(self.__header):
            return None
        return self.__header
