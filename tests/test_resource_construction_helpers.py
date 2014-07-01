import unittest
from whistle.handler import Handler
from whistle import resource_construction_helpers


class TestResourceConstructionHelper(unittest.TestCase):

    def test_is_pipeline_success(self):
        result = resource_construction_helpers.is_pipeline([Handler()])
        self.assertTrue(result)

    def test_is_pipeline_failure(self):
        result = resource_construction_helpers.is_pipeline([object()])
        self.assertFalse(result)

    def test_is_pipeline_failure_one_handler(self):
        result = resource_construction_helpers.is_pipeline(
            [object(), Handler()])
        self.assertFalse(result)

    def test_is_pipeline_failure_not_list(self):
        result = resource_construction_helpers.is_pipeline(Handler())
        self.assertFalse(result)
