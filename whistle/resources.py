
"""
A resource defines an object that exposes CRUD functionality on an entity.
CRUD operations can be at detail level as well as list level. CRUD list
operations enable bulk operations.

Currently we will not support any bulk operation optimizations at the repo
level. When we do that, it should be simple enough to make the resource use
them
"""
import six


class ResourceOptions(object):
    """
    A configuration class for the resource. Provides sane defaults for options
    that can be over-ridden by the Meta class in a resource
    """

    def __init__(self, options):
        self.options = options
        for opt_name in dir(options):
            if not opt_name.startswith('_'):
                setattr(self, opt_name, getattr(options, opt_name))


class ResourceMetaClass(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(ResourceMetaClass, cls).__new__(
            cls, name, bases, attrs)
        options = getattr(new_class, 'Meta', None)
        new_class._meta = ResourceOptions(options)

        if getattr(new_class._meta, 'resource_name', None) is None:
            # resource_name is not provided. auto-name the resource.
            class_name = new_class.__name__
            name_bits = [bit for bit in class_name.split('Resource') if bit]
            resource_name = ''.join(name_bits).lower()
            new_class._meta.resource_name = resource_name
        return new_class


class Resource(six.with_metaclass(ResourceMetaClass)):

    def _create_request(self, requesting_user, params):
        """
        Given a requesting user and the params of the request, builds a request
        object. Request object is passed around all the internal functions and
        contains all the information
        """
        pass

    def process_filters(self, requesting_user, filters):
        """
        A hook to modify the filters passed to the repo. This is a good place
        to restrict the set of accessible objects based on the user making
        the request
        """
        return filters

    def get_object(self, requesting_user, id):
        applicable_filters = dict(id=id)
        applicable_filters = self.process_filters(
            requesting_user, applicable_filters)
