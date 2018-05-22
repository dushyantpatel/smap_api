class ValueNotFoundError(Exception):
    def __init__(self, *args):
        super(ValueNotFoundError, self).__init__(*args)