class HTTP_400_Exception(Exception):
    def __init__(self, *args):
        super(HTTP_400_Exception, self).__init__(*args)