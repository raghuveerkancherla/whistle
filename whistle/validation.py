

class RequestValidation(object):
    """
    Helps validation of a request. Each resource is configured to have
    RequestValidation. Before and after a pipeline handler function is called,
    corresponding request validation function is called.
    For example is a handler function is called get_obj,
    pre_get_obj and post_get_obj validation functions are called on
    RequestValidation object
    """

    def __init__(self, request):
        self.request = request
