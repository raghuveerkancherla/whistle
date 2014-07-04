import unittest
from whistle.action_groups import ActionGroup
from whistle.actions import Action
from mock import MagicMock


class TestActionGroup(unittest.TestCase):

    def setUp(self):
        self.callable1 = MagicMock(spec=Action)
        self.callable2 = MagicMock(spec=Action)
        self.callable3 = MagicMock()

        class TestActionGroup(ActionGroup):
            name = 'TestActionGroup'
            create = self.callable1
            update = self.callable2

        class InvalidActionGroup(ActionGroup):
            name = 'InvalidActionGroup'
            create = self.callable3

        class NameLessActionGroup(ActionGroup):
            create = self.callable2

        self.TestActionGroup = TestActionGroup
        self.InvalidActionGroup = InvalidActionGroup
        self.NameLessActionGroup = NameLessActionGroup

    def test_handler_is_called(self):
        action_group = self.TestActionGroup()

        action_group.create(arg1=1, arg2=2)

        self.callable1.assert_called_once_with(arg1=1, arg2=2)
        self.assertEqual(self.callable2.call_count, 0)

    def test_all_actions_are_callable(self):
        action_group = self.TestActionGroup()

        action_group.create(arg1=1, arg2=2)
        action_group.update(arg1=3, arg2=4)

        self.callable1.assert_called_once_with(arg1=1, arg2=2)
        self.callable2.assert_called_once_with(arg1=3, arg2=4)

    def test_empty_actiongroup_not_allowed(self):
        self.assertRaises(TypeError, self.InvalidActionGroup)

    def test_nameless_actiongroup_not_allowed(self):
        self.assertRaises(TypeError, self.NameLessActionGroup)
