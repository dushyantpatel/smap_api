class IncorrectRequestFormatError(Exception):
    def __init__(self, *args):
        super(IncorrectRequestFormatError, self).__init__(*args)