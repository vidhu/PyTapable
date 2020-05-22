from functools import partial, wraps
from .hooks import BaseHook, Tap, HookConfig


class FunctionalTap(Tap):
    def __init__(self, name, fn, before, after):
        super(FunctionalTap, self).__init__(name, fn)
        self.before = before
        self.after = after


class FunctionalBaseHook(BaseHook):
    HOOK_TYPE = BaseHook.FUNCTIONAL

    def tap(self, name, fn, before=True, after=True):
        tap = FunctionalTap(
            name=name,
            fn=fn,
            before=before,
            after=after
        )
        tap = self.interceptor.register(tap) if self.interceptor else tap
        self.taps.append(tap)

    def call_taps(self, fn_args, is_before, fn_output=None):
        for tap in self.taps:
            if (tap.before and is_before) or (tap.after and not is_before):
                tap.fn(
                    fn_args=fn_args,
                    fn_output=fn_output,
                    context={
                        'hook_type': FunctionalBaseHook.HOOK_TYPE,
                        'hook_type_label': self.label,
                        'tap_name': tap.name,
                        'is_before': is_before
                    }
                )


class HookableMixin(object):
    def __init__(self, *args, **kwargs):
        super(HookableMixin, self).__init__(*args, **kwargs)
        self.hooks = {}
        klass = type(self)
        for method in map(partial(getattr, klass), dir(klass)):
            if hasattr(method, '_pytapable'):
                hook_config = getattr(method, '_pytapable')
                self.hooks[hook_config.name] = FunctionalBaseHook(
                    interceptor=hook_config.interceptor
                )

    def inherit_hooks(self, hookable_instance):
        self.hooks.update(hookable_instance.hooks)


class CreateHook(object):
    def __init__(self, name=None, interceptor=None):
        self.name = name
        self.interceptor = interceptor

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            hook = args[0].hooks[self.name]
            fn_args = {"args": args, "kwargs": kwargs}

            hook.call_taps(fn_args=fn_args, fn_output=None, is_before=True)

            out = fn(*args, **kwargs)

            hook.call_taps(fn_args=fn_args, fn_output=out, is_before=False)

            return out

        hook_config = HookConfig(name=self.name, interceptor=self.interceptor)
        wrapper._pytapable = hook_config
        return wrapper

    def get_name(self):
        return
