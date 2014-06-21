
"""
A resource defines an object that exposes CRUD functionality on an entity.
CRUD operations can be at detail level as well as list level. CRUD list
operations enable bulk operations.

Currently we will not support any bulk operation optimizations at the repo
level. When we do that, it should be simple enough to make the resource use
them
"""
import six
from whistle.request import Request
from functools import partial


class ResourceOptions(object):
    """
    A configuration class for the resource. Provides sane defaults for options
    that can be over-ridden by the Meta class in a resource

    @handlers: a map of handler_name to callable. resource.handler_name will
    call the callable with a request object. The handler is expected to return
    a response object

    @serializer (Class): object of this class should be able to serialize the
    response from the handlers

    @validator (Class): object of this class should be able to validate the
    request. Authorization, update and create request data validation,
    business validations (is this update even allowed etc) are all expected
    to be handled by a validator
    """

    def __init__(self, options):
        self.options = options
        self.handlers = {}
        self.serializer = None  # set this to default serializer later on
        self.validator = None

        for opt_name in dir(options):
            if not opt_name.startswith('_'):
                setattr(self, opt_name, getattr(options, opt_name))


class ResourceMetaClass(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(ResourceMetaClass, cls).__new__(
            cls, name, bases, attrs)
        options = getattr(new_class, 'Meta', None)
        new_class._meta = ResourceOptions(options)

        #  Not sure this is required yet!
        if getattr(new_class._meta, 'resource_name', None) is None:
            # resource_name is not provided. auto-name the resource.
            class_name = new_class.__name__
            name_bits = [bit for bit in class_name.split('Resource') if bit]
            resource_name = ''.join(name_bits).lower()
            new_class._meta.resource_name = resource_name

        return new_class


class Resource(six.with_metaclass(ResourceMetaClass)):

    def call_handler(self, fn, user=None, **kwargs):
        """
        used when "resource_obj"."handler_name" is accessed. A partial of this
        function is returned on attribute access.
        """
        request = Request(user=user, params=kwargs)
        response = fn(request=request)
        return response  # this should be serialized and returned later on

    def __getattr__(self, name):
        """
        check if a handler is being accessed. If yes check if it is a callable
        and return a partial that will construct the request and call the
        handler with it.
        """
        handlers = self._meta.handlers
        if name in handlers and callable(handlers[name]):
            return partial(self.call_handler, fn=handlers[name])
        else:
            super(Resource, self).__getattr__(name)
