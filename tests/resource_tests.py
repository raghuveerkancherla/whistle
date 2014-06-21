import unittest
from mock import MagicMock
from whistle.resources import Resource
from whistle.request import Request


class TestResource2(Resource):
    pass


get_obj_func = MagicMock()


class TestResource(Resource):

    class Meta:
        resource_name = 'new_resource'
        asdf = 'asdf'
        handlers = {
            'get_obj': get_obj_func,
        }


class TestResourceConstruction(unittest.TestCase):

    def test_resource_name(self):
        self.assertEqual(TestResource._meta.resource_name, 'new_resource')

    def test_dummy_property_on_meta(self):
        self.assertEqual(TestResource._meta.asdf, 'asdf')

    def test_default_settings(self):
        test_resource = TestResource2()
        self.assertEqual(test_resource._meta.validator, None)
        self.assertEqual(test_resource._meta.handlers, {})
        self.assertEqual(test_resource._meta.serializer, None)


class TestResourceHandlers(unittest.TestCase):

    def test_handler_is_called(self):
        test_resource = TestResource()
        test_resource.get_obj(somearg1=1, somearg2=2)

        expected_request = Request(user=None,
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        get_obj_func.assert_called_with(request=expected_request)
