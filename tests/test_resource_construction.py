import unittest
from whistle.resources import Resource
from whistle.handler import Handler


get_handler = Handler()
post_handler = Handler()


class TestResource(Resource):

    get = [get_handler]
    post = [post_handler]

    class Meta:
        resource_name = 'new_resource'
        asdf = 'asdf'


class TestResourceConstruction(unittest.TestCase):

    def test_dummy_property_on_meta(self):
        self.assertEqual(TestResource._meta.resource_name, 'new_resource')
        self.assertEqual(TestResource._meta.asdf, 'asdf')

    def test_handlers(self):
        test_resource = TestResource()

        self.assertTrue('post' in test_resource.pipeline_methods.keys())
        self.assertTrue('get' in test_resource.pipeline_methods.keys())
        self.assertEqual(test_resource.pipeline_methods['get'],
                         [get_handler])
        self.assertEqual(test_resource.pipeline_methods['post'],
                         [post_handler])
