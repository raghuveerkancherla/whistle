import unittest
from mock import MagicMock
from whistle.handlers import Handler
from whistle.actions import Action
from whistle.request import Request
from whistle.response import Response


class TestAction(unittest.TestCase):

    def setUp(self):
        self.get_obj = MagicMock(spec=Handler)
        self.del_obj = MagicMock(spec=Handler)

        self.get_obj.handle_response = MagicMock()
        self.get_obj.handle_request = MagicMock()
        self.get_obj.handle_request.return_value = Response()
        self.get_obj.handle_response.return_value = Response()

        self.del_obj.handle_response = MagicMock()
        self.del_obj.handle_request = MagicMock()
        self.del_obj.handle_request.return_value = Response()
        self.del_obj.handle_response.return_value = Response()

        class TestAction1(Action):
            name = 'TestAction1'
            pipeline = [self.get_obj]

        class TestAction2(Action):
            name = 'TestAction2'
            pipeline = [self.get_obj, self.del_obj]

        self.TestAction1 = TestAction1
        self.TestAction2 = TestAction2

    def test_empty_pipeline_not_allowed(self):
        class TestEmptyPipeline(Action):
            name = 'asdf'
            pass

        self.assertRaises(TypeError, TestEmptyPipeline)

    def test_empty_name_not_allowed(self):
        class TestEmptyName(Action):
            pipeline = ['asdf']

        self.assertRaises(TypeError, TestEmptyName)

    def test_api_method_calls_handler(self):
        test_api_method = self.TestAction1()
        expected_request = Request(user=None,
                                   caller='test_method1',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_api_method(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)

    def test_api_method_sets_user(self):
        test_api_method = self.TestAction1()
        user = MagicMock()

        test_api_method(user=user, somearg1=1, somearg2=2)
        expected_request = Request(user=user,
                                   caller='test_method1',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)

    def test_api_method_calls_all_functions_in_pipeline(self):
        test_api_method = self.TestAction2()
        expected_request = Request(user=None,
                                   caller='test_method2',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        expected_response = Response()
        self.get_obj.handle_request.return_value = expected_request
        self.del_obj.handle_request.return_value = expected_response
        self.del_obj.handle_response.return_value = expected_response
        self.get_obj.handle_response.return_value = expected_response

        test_api_method(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)
        self.del_obj.handle_request.assert_called_with(
            request=expected_request)
        self.get_obj.handle_response.assert_called_with(
            response=expected_response)
        self.del_obj.handle_response.assert_called_with(
            response=expected_response)

    def test_api_method_exits_pipeline_on_response(self):
        test_method = self.TestAction2()
        expected_response = Response()
        expected_request = Request(user=None,
                                   caller='test_method2',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.handle_request.return_value = expected_response

        test_method(somearg1=1, somearg2=2)

        self.get_obj.handle_request.assert_called_with(
            request=expected_request)
        self.get_obj.handle_response.assert_called_with(
            response=expected_response)
        self.assertEqual(self.del_obj.handle_request.call_count, 0)
        self.assertEqual(self.del_obj.handle_response.call_count, 0)

    def test_api_method_throws_if_no_response_from_last_handler(self):
        test_method = self.TestAction2()
        expected_request = Request(
            user=None, caller='multiple_funcs', params={})
        self.get_obj.handle_request.return_value = expected_request
        self.del_obj.handle_request.return_value = expected_request

        self.assertRaises(AssertionError, test_method,
                          somearg1=1, somearg2=2)

    def test_api_method_throws_for_non_standard_response(self):
        test_method = self.TestAction1()
        self.get_obj.handle_request.return_value = object()

        self.assertRaises(AssertionError, test_method, somearg1=1, somearg2=2)
