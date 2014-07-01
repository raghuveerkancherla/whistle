import unittest
from mock import MagicMock
from whistle.resources import Resource
from whistle.request import Request
from whistle.response import Response
from whistle.handler import Handler


class TestResourceHandlers(unittest.TestCase):

    def setUp(self):
        self.get_obj = MagicMock()
        self.del_obj = MagicMock()
        self.get_obj.handle_response = MagicMock()
        self.get_obj.handle_request = MagicMock()
        self.get_obj.handle_request.return_value = Response()
        self.get_obj.handle_response.return_value = Response()

        self.del_obj.handle_response = MagicMock()
        self.del_obj.handle_request = MagicMock()
        self.del_obj.handle_request.return_value = Response()
        self.del_obj.handle_response.return_value = Response()

        class TestResource(Resource):
            single_func = [Handler()]
            multiple_funcs = [Handler(), Handler()]

        self.TestResource = TestResource
        self.TestResource.pipeline_methods['single_func'] = [self.get_obj]
        self.TestResource.pipeline_methods['multiple_funcs'] = [self.get_obj,
                                                                self.del_obj]

    def test_handler_is_called(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='single_func',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_resource.single_func(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)

    def test_handler_sets_user(self):
        test_resource = self.TestResource()
        user = MagicMock()
        test_resource.single_func(user=user, somearg1=1, somearg2=2)

        expected_request = Request(user=user,
                                   call='single_func',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)

    def test_handler_pipeline_calls_all_functions(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        expected_response = Response()
        self.get_obj.handle_request.return_value = expected_request
        self.del_obj.handle_request.return_value = expected_response
        self.del_obj.handle_response.return_value = expected_response
        self.get_obj.handle_response.return_value = expected_response

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)
        self.del_obj.handle_request.assert_called_with(
            request=expected_request)
        self.get_obj.handle_response.assert_called_with(
            response=expected_response)
        self.del_obj.handle_response.assert_called_with(
            response=expected_response)

    def test_handler_pipeline_exits_on_response(self):
        test_resource = self.TestResource()
        expected_response = Response()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.handle_request.return_value = expected_response

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)
        self.get_obj.handle_response.assert_called_with(
            response=expected_response)
        self.assertEqual(self.del_obj.handle_request.call_count, 0)
        self.assertEqual(self.del_obj.handle_response.call_count, 0)

    def test_call_throws_if_no_response_from_last_handler(self):
        test_resource = self.TestResource()
        expected_request = Request(
            user=None, call='multiple_funcs', params={})
        self.get_obj.handle_request.return_value = expected_request
        self.del_obj.handle_request.return_value = expected_request

        with self.assertRaises(AssertionError):
            test_resource.multiple_funcs(somearg1=1, somearg2=2)

    def test_call_throws_for_non_standard_response_from_handler(self):
        test_resource = self.TestResource()
        self.get_obj.handle_request.return_value = object()

        with self.assertRaises(AssertionError):
            test_resource.multiple_funcs(somearg1=1, somearg2=2)
