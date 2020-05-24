from unittest import TestCase
from .common_mock import patch

from types import FunctionType
from pytapable import HookableMixin, CreateHook, HookInterceptor, Tap, Hook


HOOK_MOVE = 'move_hook_name'
TAP_NAME = 'my_tap'


class CarHookInterceptor(HookInterceptor):

    def register(self, tap):
        pass


interceptor = CarHookInterceptor()


class Car(HookableMixin):

    @CreateHook(HOOK_MOVE, interceptor)
    def move(self, *args, **kargs):
        return "MOVING"


class HookInterceptorTests(TestCase):

    def test_register_functional(self):
        c = Car()

        modified_tap = 'modified_tap'
        with patch.object(interceptor, 'register', return_value=modified_tap) as mock_register:
            c.hooks[HOOK_MOVE].tap(TAP_NAME, lambda: None)

        assert mock_register.called

        tap = mock_register.call_args_list[0][0][0]
        assert isinstance(tap, Tap)
        assert tap.name == TAP_NAME
        assert isinstance(tap.fn, FunctionType)

        assert c.hooks[HOOK_MOVE].taps[0] == modified_tap

    def test_register_inline(self):
        my_hook = Hook(interceptor)

        # Tap into hook to trigger register intercept
        modified_tap = 'modified_tap'
        with patch.object(interceptor, 'register', return_value=modified_tap) as mock_register:
            my_hook.tap(TAP_NAME, lambda: None)

        assert mock_register.called
        tap = mock_register.call_args_list[0][0][0]
        assert isinstance(tap, Tap)
        assert tap.name == TAP_NAME
        assert isinstance(tap.fn, FunctionType)

        assert my_hook.taps[0] == modified_tap





