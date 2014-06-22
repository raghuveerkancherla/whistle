import unittest
from mock import MagicMock
from whistle.resources import Resource
from whistle.request import Request
from whistle.response import Response


class TestResourceHandlers(unittest.TestCase):

    def setUp(self):
        self.get_obj = MagicMock()
        self.del_obj = MagicMock()

        class TestResource(Resource):

            class Meta:
                handlers = {
                    'single_func': [self.get_obj],
                    'multiple_funcs': [self.get_obj, self.del_obj]
                }

        self.TestResource = TestResource

    def test_handler_is_called(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='single_func',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_resource.single_func(somearg1=1, somearg2=2)

        self.get_obj.assert_called_with(request=expected_request)

    def test_handler_sets_user(self):
        test_resource = self.TestResource()
        user = MagicMock()
        test_resource.single_func(user=user, somearg1=1, somearg2=2)

        expected_request = Request(user=user,
                                   call='single_func',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.assert_called_with(request=expected_request)

    def test_handler_pipeline_calls_all_functions(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        expected_response = Response()
        self.get_obj.return_value = expected_request
        self.del_obj.return_value = expected_response

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        self.get_obj.assert_called_with(request=expected_request)
        self.del_obj.assert_called_with(request=expected_request)

    def test_handler_pipeline_exits_on_response(self):
        test_resource = self.TestResource()
        expected_response = Response()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.return_value = expected_response

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        self.get_obj.assert_called_with(request=expected_request)
        self.assertEqual(self.del_obj.call_count, 0)
