
"""
A resource defines an object that exposes functionality. It allows the
definition of handler that can be called on the resource.
"""
import six
from whistle.request import Request
from whistle.response import Response
from whistle import resource_construction_helpers
from functools import partial


class ResourceOptions(object):

    """
    A configuration class for the resource. Provides sane defaults for options
    that can be over-ridden by the Meta class in a resource

    @handlers: a map of handler_name to a list of handler objects.
    resource.handler_name will call each handler with a request object.
    The handler is expected to return a response object

    @serializer (Class): object of this class should be able to serialize the
    response from the handlers

    """

    def __init__(self, options):
        self.options = options
        self.serializer = None  # set this to default serializer later on

        for opt_name in dir(options):
            if not opt_name.startswith('_'):
                setattr(self, opt_name, getattr(options, opt_name))


class ResourceMetaClass(type):

    def __new__(cls, name, bases, attrs):
        attrs['pipeline_methods'] = {}
        declared_methods = {}

        # Inherit any resource methods from a parent or parents
        try:
            parents = [b for b in bases if issubclass(b, Resource)]
            # MRO.
            parents.reverse()

            for p in parents:
                inherited_methods = getattr(p, 'pipeline_methods', {})

                for pipeline_method, pipeline in inherited_methods.iteritems():
                    attrs['pipeline_methods'][pipeline_method] = pipeline
        except NameError:
            pass

        for pipeline_method, pipeline in attrs.items():
            if resource_construction_helpers.is_pipeline(pipeline):
                pipeline = attrs.pop(pipeline_method)
                declared_methods[pipeline_method] = pipeline

        attrs['pipeline_methods'].update(declared_methods)
        attrs['declared_methods'] = declared_methods

        new_class = super(ResourceMetaClass, cls).__new__(
            cls, name, bases, attrs)
        options = getattr(new_class, 'Meta', None)
        new_class._meta = ResourceOptions(options)

        return new_class


class Resource(six.with_metaclass(ResourceMetaClass)):

    def call_handler(self, pipeline, call, user=None, **kwargs):
        """
        used when "resource_obj"."method_name" is accessed. A partial of this
        function is returned on attribute access.
        """
        request = Request(user=user, params=kwargs, call=call)

        for counter, handler in enumerate(pipeline):
            response = handler.handle_request(request=request)
            assert type(response) in [Request, Response],\
                "handle_request of {} handler did"\
                " not return a request or a response object".format(
                    handler.name)
            if isinstance(response, Response):
                break

        assert isinstance(response, Response),\
            "pipeline of {} did"\
            " not return a response object".format(call)

        run_pipeline = pipeline[:counter + 1]
        for handler in reversed(run_pipeline):
            response = handler.handle_response(response=response)
            assert isinstance(response, Response),\
                "handle_response of {} handler did"\
                " not return a response object".format(handler.name)
        return response  # this should be serialized and returned later on

    def __getattr__(self, name):
        """
        check if a handler is being accessed. If yes check if it is a callable
        and return a partial that will construct the request and call the
        handler with it.
        """
        pipeline_methods = self.pipeline_methods
        if name in pipeline_methods:
            pipeline = pipeline_methods[name]
            return partial(self.call_handler,
                           pipeline=pipeline,
                           call=name)
        else:
            return object.__getattribute__(self, name)
