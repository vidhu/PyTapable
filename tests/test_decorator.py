from unittest import TestCase
from unittest.mock import MagicMock

from pytapable import HookableMixin, CreateHook, BaseHook

HOOK_MOVE = 'move_hook_name'
TAP_NAME = 'my_tap'


class Car(HookableMixin):

    @CreateHook(HOOK_MOVE)
    def move(self, *args, **kargs):
        return "MOVING"


class TestInstanceLevelHooks(TestCase):

    def test_create_hook(self):
        c = self.create_instance()

        assert len(c.hooks) == 1
        assert c.hooks[HOOK_MOVE].HOOK_TYPE == BaseHook.FUNCTIONAL
        assert c.hooks[HOOK_MOVE].label == BaseHook.HOOK_TYPE_LABEL[BaseHook.FUNCTIONAL]

    def test_install_tap(self):
        c = self.create_instance()
        callback = self.install_tap(c)

        assert len(c.hooks[HOOK_MOVE].taps) == 1
        assert c.hooks[HOOK_MOVE].taps[0].name == TAP_NAME
        assert c.hooks[HOOK_MOVE].taps[0].fn == callback

    def test_trigger_hook_pre_and_post(self):
        c = self.create_instance()
        callback = self.install_tap(c)

        return_val = c.move('100pmh', reverse=True)

        assert return_val == 'MOVING'
        assert callback.call_count == 2  # pre and post call

        # Pre Call
        callback.assert_any_call(
            fn_args={
                'args': (c, '100pmh'),
                'kwargs': {'reverse': True}
            },
            fn_output=None,
            context={
                'hook_type': BaseHook.FUNCTIONAL,
                'hook_type_label': BaseHook.HOOK_TYPE_LABEL[BaseHook.FUNCTIONAL],
                'tap_name': TAP_NAME,
                'is_before': True
            }
        )

        # Post Call
        callback.assert_any_call(
            fn_args={
                'args': (c, '100pmh'),
                'kwargs': {'reverse': True}
            },
            fn_output="MOVING",
            context={
                'hook_type': BaseHook.FUNCTIONAL,
                'hook_type_label': BaseHook.HOOK_TYPE_LABEL[BaseHook.FUNCTIONAL],
                'tap_name': TAP_NAME,
                'is_before': False
            }
        )

    def test_trigger_hook_only_pre(self):
        c = self.create_instance()
        callback = self.install_tap(c, after=False)

        return_val = c.move('100pmh', reverse=True)

        assert return_val == 'MOVING'
        assert callback.call_count == 1  # pre and post call

        # Pre Call
        callback.assert_any_call(
            fn_args={
                'args': (c, '100pmh'),
                'kwargs': {'reverse': True}
            },
            fn_output=None,
            context={
                'hook_type': BaseHook.FUNCTIONAL,
                'hook_type_label': BaseHook.HOOK_TYPE_LABEL[BaseHook.FUNCTIONAL],
                'tap_name': TAP_NAME,
                'is_before': True
            }
        )

    def test_trigger_hook_only_post(self):
        c = self.create_instance()
        callback = self.install_tap(c, before=False)

        return_val = c.move('100pmh', reverse=True)

        assert return_val == 'MOVING'
        assert callback.call_count == 1  # post call

        # Post Call
        callback.assert_any_call(
            fn_args={
                'args': (c, '100pmh'),
                'kwargs': {'reverse': True}
            },
            fn_output="MOVING",
            context={
                'hook_type': BaseHook.FUNCTIONAL,
                'hook_type_label': BaseHook.HOOK_TYPE_LABEL[BaseHook.FUNCTIONAL],
                'tap_name': TAP_NAME,
                'is_before': False
            }
        )

    @classmethod
    def create_instance(cls):
        return Car()

    @classmethod
    def install_tap(cls, instance, **kwargs):
        callback = MagicMock()
        instance.hooks[HOOK_MOVE].tap(TAP_NAME, callback, **kwargs)
        return callback
