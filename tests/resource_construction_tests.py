import unittest
from whistle.resources import Resource


class TestResource(Resource):

    class Meta:
        resource_name = 'new_resource'
        asdf = 'asdf'


class TestResourceConstruction(unittest.TestCase):

    def test_resource_name(self):
        self.assertEqual(TestResource._meta.resource_name, 'new_resource')

    def test_dummy_property_on_meta(self):
        self.assertEqual(TestResource._meta.asdf, 'asdf')

    def test_default_settings(self):
        test_resource = TestResource()
        self.assertEqual(test_resource._meta.validator, None)
        self.assertEqual(test_resource._meta.handlers, {})
        self.assertEqual(test_resource._meta.serializer, None)
