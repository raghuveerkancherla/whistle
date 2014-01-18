
class InvalidCallable(Exception):
    '''
    Raised when an invalid callable object is registered with api
    callable is invalid when 
     1. its name is invalid.
     2. it does not have an _meta attribute with a name parameter
    '''
    pass
