class HTTP_204_Exception(Exception):
    def __init__(self, *args):
        super(HTTP_204_Exception, self).__init__(*args)