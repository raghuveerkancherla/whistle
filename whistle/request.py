
class Request(object):
    """
    All user facing functions in a Resource like get_detail, get_list etc. are
    called with a requesting user and other parameters. These details are
    wrapped in a request object to deal with these parameters
    """
    def __init__(self, user, params, caller):
        self.user = user
        self.params = params
        self.caller = caller

    def __eq__(self, val):
        return self.user == val.user and self.params == val.params
