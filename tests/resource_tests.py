import unittest
from whistle.resources import Resource


class TestResource2(Resource):

    class Meta:
        entity = 'new_entity2'
        entity_repo = 'new_entity_repo2'


class TestResource(Resource):

    class Meta:
        entity = 'new_entity'
        entity_repo = 'new_entity_repo'
        resource_name = 'new_resource'
        asdf = 'asdf'


class TestResourceConstruction(unittest.TestCase):

    def test_meta_is_processed(self):
        self.assertEqual(TestResource._meta.entity, 'new_entity')
        self.assertEqual(TestResource._meta.entity_repo, 'new_entity_repo')

    def test_resource_name_is_computed(self):
        self.assertEqual(TestResource2._meta.resource_name, 'test2')

    def test_resource_name(self):
        self.assertEqual(TestResource._meta.resource_name, 'new_resource')

    def test_dummy_property_on_meta(self):
        self.assertEqual(TestResource._meta.asdf, 'asdf')


class TestResourceCRUD(unittest.TestCase):

    def test_get_object(self):
        pass