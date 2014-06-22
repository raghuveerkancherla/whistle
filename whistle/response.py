
class Response(object):

    def __init__(self, is_success=True, meta=None, data=None):
        self.is_success = is_success
        self.data = data
        self.meta = meta
