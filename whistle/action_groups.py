import six
from whistle.actions import Action
from functools import partial


class ActionGroupMetaClass(type):

    def __new__(cls, name, bases, attrs):
        attrs['_actions'] = {}
        declared_actions = {}

        # Inherit any fields from parent(s).
        try:
            parents = [b for b in bases if issubclass(b, Resource)]
            # Simulate the MRO.
            parents.reverse()

            for p in parents:
                actions_declared_on_parent = getattr(p, '_actions', {})

                for action_name, action in actions_declared_on_parent.items():
                    attrs['_actions'][action_name] = action
        except NameError:
            pass

        for action_name, action_obj in attrs.items():
            if isinstance(action_obj, Action):
                action_obj = attrs.pop(action_name)
                declared_actions[action_name] = action_obj

        attrs['_actions'].update(declared_actions)
        attrs['_declared_actions'] = declared_actions

        return super(ActionGroupMetaClass, cls).__new__(cls, name, bases, attrs)


class ActionGroup(six.with_metaclass(ActionGroupMetaClass)):
    """
    ActionGroup allows grouping of related actions in an API.
    For example CRUD api's can group create, update, delete,
    and read actions into one action group.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'name'):
            raise TypeError('Missing property `name` on Action Group `{group_name}`'.format(group_name=cls.__name__))
        obj = super(ActionGroup, cls).__new__(cls, *args, **kwargs)
        if len(obj.get_actions()) == 0:
            raise TypeError('No actions defined on ActionGroup `{group_name}`'.format(group_name=cls.__name__))
        return obj

    def get_actions(self):
        return self._actions

    def call_handler(self, action, *args, **kwargs):
        return action(*args, **kwargs)

    def __getattr__(self, name):
        """
        check if an action is being accessed. If yes return a partial that
        will construct the request and call the action with it.
        """
        actions = self.get_actions()
        if name in actions:
            # This is an action
            action = actions[name]
            return partial(self.call_handler, action=action)
        else:
            return object.__getattribute__(self, name)
