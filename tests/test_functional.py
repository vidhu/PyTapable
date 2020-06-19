from unittest import TestCase
from .common_mock import MagicMock

from pytapable import HookableMixin, CreateHook, BaseHook, create_hook_name, create_hook_names, Hook

HOOK_MOVE = 'move_hook_name'
TAP_NAME = 'my_tap'


class Car(HookableMixin):

    @CreateHook(HOOK_MOVE)
    def move(self, *args, **kargs):
        return "MOVING"


class TestInstanceLevelHooks(TestCase):

    @classmethod
    def create_instance(cls):
        return Car()

    @classmethod
    def install_tap(cls, instance, **kwargs):
        callback = MagicMock()
        instance.hooks[HOOK_MOVE].tap(TAP_NAME, callback, **kwargs)
        return callback

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
            fn_args=(c, '100pmh'),
            fn_kwargs={'reverse': True},
            fn_output=None,
            context={
                'hook': c.hooks[HOOK_MOVE],
                'tap': c.hooks[HOOK_MOVE].taps[0],
                'is_before': True
            }
        )

        # Post Call
        callback.assert_any_call(
            fn_args=(c, '100pmh'),
            fn_kwargs={'reverse': True},
            fn_output="MOVING",
            context={
                'hook': c.hooks[HOOK_MOVE],
                'tap': c.hooks[HOOK_MOVE].taps[0],
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
            fn_args=(c, '100pmh'),
            fn_kwargs={'reverse': True},
            fn_output=None,
            context={
                'hook': c.hooks[HOOK_MOVE],
                'tap': c.hooks[HOOK_MOVE].taps[0],
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
            fn_args=(c, '100pmh'),
            fn_kwargs={'reverse': True},
            fn_output="MOVING",
            context={
                'hook': c.hooks[HOOK_MOVE],
                'tap': c.hooks[HOOK_MOVE].taps[0],
                'is_before': False
            }
        )

    def test_create_hook_name(self):
        name = 'MY_HOOK'
        hook1 = create_hook_name(name)
        hook2 = create_hook_name(name)
        hook3 = create_hook_name()

        assert hook1 != hook2
        assert name in hook1
        assert name in hook2
        assert hook3 != ''

    def test_create_hook_names(self):
        (hook1, hook2, hook3) = create_hook_names(*range(3))

        assert len({hook1, hook2, hook3}) == 3

        for hook in [hook1, hook2, hook3]:
            assert hook != ''
