from .exceptions import InvalidCallable
import utils

class Api(object):
    '''
    Api object that registers all interactors together.
    This is the object via which all business logic will be used in other applications.
    Other parts of an application - like the http api, command line interface 
    etc will likely use this object
    '''

    def __init__(self, version):
        self.version = version
        self._registry = {}

    def register(self, callable_object):
        '''
        Registers 
        '''
        try:
            if callable(callable_object) and utils.is_alphanum(\
                    callable_object._meta.name):
                self._registry[callable_object._meta.name] = callable_object
            else:
                raise InvalidCallable('%s is not a valid name' %callable_object._meta.name)
        except AttributeError, e:
                '''
                Happens if callable_object does not have _meta or _meta.name properties
                '''
                raise InvalidCallable(e)

    def __getattr__(self, prop):
        if prop in self._registry:
            return self._registry[prop]
