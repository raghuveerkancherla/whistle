from abc import ABCMeta, abstractproperty
import six
from whistle.request import Request
from whistle.response import Response


class ApiMethod(six.with_metaclass(ABCMeta)):

    #subclasses should set pipeline for the method to function properly.

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def pipeline(self):
        pass

    def __new__(cls, *args, **kwargs):
        obj = super(ApiMethod, cls).__new__(cls, *args, **kwargs)
        if len(cls.pipeline) == 0:
            raise TypeError(u"Can't instantiate {} with empty pipeline".format(
                cls.__name__))

        return obj

    def __call__(self, user=None, *args, **kwargs):
        request = Request(user=user, params=kwargs, caller=self.name)

        for counter, handler in enumerate(self.pipeline):
            response = handler.handle_request(request=request)
            assert type(response) in [Request, Response],\
                "handle_request of {handler_name} handler did not return a request or a response object".format(
                    handler_name=handler.name)
            if isinstance(response, Response):
                break

        assert isinstance(response, Response),\
            "pipeline of {handler_name} did not return a response object".format(handler_name=self.name)

        run_pipeline = self.pipeline[:counter + 1]
        for handler in reversed(run_pipeline):
            response = handler.handle_response(response=response)
            assert isinstance(response, Response),\
                "handle_response of {handler_name} handler did not return a response object".format(
                    handler_name=handler.name)
        return response  # this should be serialized and returned later on
