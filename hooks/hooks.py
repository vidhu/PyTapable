from typing import List
import uuid
from functools import wraps, partial


class Tap(object):
    def __init__(self, name, fn, before, after):
        self.name = name
        self.fn = fn
        self.before = before
        self.after = after


class Hook(object):
    def __init__(self):
        self.taps = []  # type: List[Tap]
        self.interceptor = None

    def tap(self, name, fn, before=True, after=True):
        self.taps.append(Tap(
            name=name,
            fn=fn,
            before=before,
            after=after
        ))

    def __call__(self, *args, **kwargs):
        self.tap(*args, **kwargs)

    def call(self, fn_args, is_before, fn_output=None):
        for tap in self.taps:
            if (tap.before and is_before) or (tap.after and not is_before):
                tap.fn(
                    fn_args=fn_args,
                    fn_output=fn_output,
                    context={
                        'name': tap.name,
                        'is_before': is_before
                    }
                )

    def intercept(self, interceptor):
        self.interceptor = interceptor


class Hookable(object):
    def __init__(self, *args, **kwargs):
        super(Hookable, self).__init__(*args, **kwargs)
        self.hooks = {}
        klass = type(self)
        for method in map(partial(getattr, klass), dir(klass)):
            if hasattr(method, '__hooked'):
                name = getattr(method, '__hooked')
                self.hooks[name] = Hook()

    def inherit_hooks(self, hookable_instance):
        self.hooks.update(hookable_instance.hooks)


class CreateHook(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            tap = args[0].hooks[self.name]
            fn_args = {"args": args, "kwargs": kwargs}

            tap.call(fn_args=fn_args, fn_output=None, is_before=True)

            out = fn(*args, **kwargs)

            tap.call(fn_args=fn_args, fn_output=out, is_before=False)

            return out

        setattr(wrapper, '__hooked', self.name)
        return wrapper

    def get_name(self):
        return


def create_hook_name(name):
    prefix = str(uuid.uuid4())
    return "{}:{}".format(prefix, name)
