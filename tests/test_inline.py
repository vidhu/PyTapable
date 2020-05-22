from unittest import TestCase
from unittest.mock import MagicMock

from pytapable import Hook

TAP_NAME = 'my_tap'


class TestInlineHooks(TestCase):

    def test_create_hook(self):
        my_hook = Hook()

        assert my_hook.HOOK_TYPE == Hook.INLINE
        assert my_hook.label == Hook.HOOK_TYPE_LABEL[Hook.INLINE]

    def test_install_tap(self):
        my_hook = Hook()

        # Tap into hook
        callback = MagicMock()
        my_hook.tap(TAP_NAME, callback)

        assert len(my_hook.taps) == 1
        assert my_hook.taps[0].name == TAP_NAME
        assert my_hook.taps[0].fn == callback

    def test_trigger_hook(self):
        my_hook = Hook()

        # Tap into hook
        callback = MagicMock()
        my_hook.tap(TAP_NAME, callback)

        # Trigger
        kwargs = {'primitive': 'hi', 'complex': {'a': 1}}
        my_hook.call_taps(**kwargs)

        callback.assert_called_once_with(**kwargs)


