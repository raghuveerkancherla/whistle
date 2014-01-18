import unittest
from ..whistle.api import Api
from ..whistle.exceptions import InvalidCallable

class CallableMeta(object):
    def __init__(self, name):
        self.name = name

class Callable(object):
    def __init__(self, name):
        self._meta = CallableMeta(name=name)

    def __call__(self, *args, **kwargs):
        return 1


class ApiObjectTest(unittest.TestCase):

    def setUp(self):
        self.api = Api(version='v1')

    def test_version(self):
        '''
        Api object accepts a string param @version which 
        will be accessible via api.version
        '''
        self.assertEqual(self.api.version, 'v1')

    def test_register(self):
        '''
        Api object allows registration of a callable object.
        callable object must have _meta object with a name property.
        '''
        callable_object = Callable('somename')
        self.api.register(callable_object)

    def test_registered(self):
        '''
        A registered object should be callable by its name.
        All args and kwargs should get passed on to the callable object
        '''
        self.test_register() #registers an object
        self.assertEqual(self.api.somename() ,1)
   
    def test_invalid_registration1(self):
        '''
        Registration of an object with invalid name raises InvalidCallable
        '''
        callable_object = Callable('some name')
        self.assertRaises(InvalidCallable, self.api.register, callable_object)

    def test_invalid_registration2(self):
        '''
        Registration of an object with _meta missing raises InvalidCallable
        '''
        self.assertRaises(InvalidCallable, self.api.register, lambda x: x)

    def test_invalid_registration3(self):
        '''
        Registration of a non callable object raises InvalidCallable
        '''
        self.assertRaises(InvalidCallable, self.api.register, 'asdf')
