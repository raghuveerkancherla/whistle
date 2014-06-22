import unittest
from mock import MagicMock
from whistle.resources import Resource
from whistle.validation import RequestValidation
from whistle.request import Request
from whistle.response import Response


class TestResourceValidation(unittest.TestCase):

    def setUp(self):
        self.get_obj = MagicMock()
        self.get_obj.__name__ = 'get_obj'
        self.del_obj = MagicMock()
        self.del_obj.__name__ = 'del_obj'
        self.pre_get_obj = MagicMock(return_value=None)
        self.post_get_obj = MagicMock(return_value=None)
        self.pre_del_obj = MagicMock(return_value=None)
        self.post_del_obj = MagicMock(return_value=None)

        class Validation(RequestValidation):
            pre_get_obj = self.pre_get_obj
            post_get_obj = self.post_get_obj

            pre_del_obj = self.pre_del_obj
            post_del_obj = self.post_del_obj

        class TestResource(Resource):

            class Meta:
                handlers = {
                    'single_func': [self.get_obj],
                    'multiple_funcs': [self.get_obj, self.del_obj]
                }
                validator = Validation

        self.TestResource = TestResource

    def test_validation_gets_called(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='single_func',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.return_value = expected_request

        test_resource.single_func(somearg1=1, somearg2=2)

        # not sure how to test pre got called before post
        self.pre_get_obj.assert_called_once_with(request=expected_request)
        self.post_get_obj.assert_called_once_with(request=expected_request)

    def test_validation_gets_called_for_entire_pipeline(self):
        test_resource = self.TestResource()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})
        self.get_obj.return_value = expected_request

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        # not sure how to test pre got called before post
        self.pre_get_obj.assert_called_once_with(request=expected_request)
        self.post_get_obj.assert_called_once_with(request=expected_request)
        self.pre_del_obj.assert_called_once_with(request=expected_request)
        self.post_del_obj.assert_called_once_with(request=expected_request)

    def test_post_validation_if_handlers_returns_response(self):
        test_resource = self.TestResource()
        self.get_obj.return_value = expected_response = Response()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        # not sure how to test pre got called before post
        self.pre_get_obj.assert_called_once_with(request=expected_request)
        self.post_get_obj.assert_called_once_with(response=expected_response)

    def test_validations_skipped_if_handler_returns_response(self):
        test_resource = self.TestResource()
        self.get_obj.return_value = expected_response = Response()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        # not sure how to test pre got called before post
        self.pre_get_obj.assert_called_once_with(request=expected_request)
        self.post_get_obj.assert_called_once_with(response=expected_response)
        self.assertEqual(self.pre_del_obj.call_count, 0)
        self.assertEqual(self.post_del_obj.call_count, 0)

    def test_validation_is_skipped_if_pre_validation_returns_response(self):
        test_resource = self.TestResource()
        self.pre_get_obj.return_value = Response()
        expected_request = Request(user=None,
                                   call='multiple_funcs',
                                   params={'somearg1': 1,
                                           'somearg2': 2})

        test_resource.multiple_funcs(somearg1=1, somearg2=2)

        # not sure how to test pre got called before post
        self.pre_get_obj.assert_called_once_with(request=expected_request)
        self.assertEqual(self.post_get_obj.call_count, 0)
        self.assertEqual(self.pre_del_obj.call_count, 0)
        self.assertEqual(self.post_del_obj.call_count, 0)
