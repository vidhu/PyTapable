from unittest import TestCase
from .common_mock import patch

from types import FunctionType
from pytapable import HookableMixin, CreateHook, HookInterceptor, Tap, Hook

HOOK_MOVE = 'move_hook_name'
TAP_NAME = 'my_tap'


class CarHookInterceptor(HookInterceptor):

    def create(self, hook):
        print(hook)

    def register(self, context, tap):
        return tap


interceptor = CarHookInterceptor()


class Car(HookableMixin):

    @CreateHook(HOOK_MOVE, interceptor)
    def move(self, *args, **kargs):
        return "MOVING"


class HookInterceptorTests(TestCase):

    def test_interceptor_no_tap_modification(self):
        my_hook = Hook(interceptor=interceptor)

        with patch.object(interceptor, 'register', wraps=interceptor.register) as wrapper_register:
            my_hook.tap(TAP_NAME, lambda: None)

        assert wrapper_register.called

        # Assert Tap
        tap = wrapper_register.call_args_list[0][1]['tap']
        assert tap == my_hook.taps[0]

        # Assert Context
        context = wrapper_register.call_args_list[0][1]['context']
        assert context['hook'] == my_hook

    def test_register_functional(self):
        c = Car()

        modified_tap = 'modified_tap'
        with patch.object(interceptor, 'register', return_value=modified_tap) as mock_register:
            c.hooks[HOOK_MOVE].tap(TAP_NAME, lambda: None)

        assert mock_register.called

        # Assert Tap properties in .register()
        tap = mock_register.call_args_list[0][1]['tap']
        assert isinstance(tap, Tap)
        assert tap.name == TAP_NAME
        assert isinstance(tap.fn, FunctionType)

        # Assert Context
        context = mock_register.call_args_list[0][1]['context']
        assert context['hook'] == c.hooks[HOOK_MOVE]

        # Assert Tap return
        assert c.hooks[HOOK_MOVE].taps[0] == modified_tap

    def test_register_inline(self):
        my_hook = Hook(interceptor=interceptor)

        # Tap into hook to trigger register intercept
        modified_tap = 'modified_tap'
        with patch.object(interceptor, 'register', return_value=modified_tap) as mock_register:
            my_hook.tap(TAP_NAME, lambda: None)

        assert mock_register.called

        # Assert Tap properties in .register()
        tap = mock_register.call_args_list[0][1]['tap']
        assert isinstance(tap, Tap)
        assert tap.name == TAP_NAME
        assert isinstance(tap.fn, FunctionType)

        # Assert Context
        context = mock_register.call_args_list[0][1]['context']
        assert context['hook'] == my_hook

        # Assert Tap return
        assert my_hook.taps[0] == modified_tap

    def test_create_functional(self):
        with patch.object(interceptor, 'create') as mock_create:
            c = Car()

        mock_create.assert_called_once_with(hook=c.hooks[HOOK_MOVE])

    def test_create_inline(self):
        with patch.object(interceptor, 'create') as mock_create:
            my_hook = Hook(interceptor=interceptor)

        mock_create.assert_called_once_with(hook=my_hook)

