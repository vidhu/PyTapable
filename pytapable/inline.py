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
        tap = self.interceptor.register(
            context={
                'hook': self
            },
            tap=tap
        ) if self.interceptor else tap
        self.taps.append(tap)

    def call(self, *args, **kwargs):
        """
        Triggers the hook which executes all the taps with a arguments passed in args, kwargs and a context dict

        .. code-block:: python

            # Arguments to a callback

           "fn_args": *args,
           "fn_kwargs": **kwargs

           context = {
             'hook': Hook,
             'tap': Tap,
           }


        """
        for tap in self.taps:
            tap.fn(
                context={
                    'hook': self,
                    'tap': tap
                },
                fn_args = args,
                fn_kwargs = kwargs
            )

