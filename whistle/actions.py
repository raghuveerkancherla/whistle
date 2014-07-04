from abc import ABCMeta, abstractproperty
import six
from whistle.handlers import Handler
from whistle.request import Request
from whistle.response import Response


class Action(six.with_metaclass(ABCMeta)):

    #subclasses should set pipeline for the method to function properly.

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def pipeline(self):
        pass

    def __new__(cls, *args, **kwargs):
        obj = super(Action, cls).__new__(cls, *args, **kwargs)
        if len(obj.get_pipeline()) == 0:
            raise TypeError("Can't instantiate {handler_name} with empty pipeline".format(handler_name=cls.__name__))

        for handler in obj.get_pipeline():
            if not isinstance(handler, Handler):
                raise TypeError("pipeline contains an object that is not an instance of Handler")

        return obj

    def get_pipeline(self):
        return self.pipeline

    def __call__(self, user=None, *args, **kwargs):
        request = Request(user=user, params=kwargs, caller=self.name)
        pipeline = self.get_pipeline()

        for counter, handler in enumerate(pipeline):
            response = handler.handle_request(request=request)
            assert type(response) in [Request, Response],\
                "handle_request of {handler_name} handler did not return a request or a response object".format(
                    handler_name=handler.name)
            if isinstance(response, Response):
                break

        assert isinstance(response, Response),\
            "pipeline of {handler_name} did not return a response object".format(handler_name=self.name)

        run_pipeline = pipeline[:counter + 1]
        for handler in reversed(run_pipeline):
            response = handler.handle_response(response=response)
            assert isinstance(response, Response),\
                "handle_response of {handler_name} handler did not return a response object".format(
                    handler_name=handler.name)
        return response  # this should be serialized and returned later on
