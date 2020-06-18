from typing import Callable

from .hooks import BaseHook, Tap


class Hook(BaseHook):
    HOOK_TYPE = BaseHook.INLINE

    def tap(self, name, fn):
        """
        Creates a :class:`Tap` for this hook

        Args:
            name (basestring): name of the tapable
            fn (Callable): callable to execute when hook is triggered
        """
        tap = Tap(name=name, fn=fn)
        tap = self.interceptor.register(tap) if self.interceptor else tap
        self.taps.append(tap)

    def call(self, *args, **kwargs):
        """
        Triggers the hook which executes all the taps with arguments passed as is
        """
        for tap in self.taps:
            context = {
                'hook_type': BaseHook.INLINE,
                'hook_type_label': self.label,
                'hook_name': self.name,
                'tap_name': tap.name
            }
            tap.fn(context=context, args=args, kwargs=kwargs)
