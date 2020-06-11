from functools import partial, wraps
from .hooks import BaseHook, Tap, HookConfig


class FunctionalTap(Tap):
    def __init__(self, name, fn, before, after):
        """
        Functional taps is used in combination with a :class:`FunctionalBaseHook`

        Args:
            name (str): Name of the tap
            fn (Callable): This will be called when the hook triggers
            before (bool): If true, this tap will be called *before* the hooked function executes
            after (bool): If true, this tap will be called *after* the hooked function executes
        """
        super(FunctionalTap, self).__init__(name, fn)
        self.before = before
        self.after = after


class FunctionalHook(BaseHook):
    """
    Functional hooks are created when :class:`CreateHook` is used to decorate a class function. When a functional
    hook is tapped, a :class:`FunctionalTap` is created. Look at :func:`FunctionalHook.call` to see how taps are
    called
    """
    HOOK_TYPE = BaseHook.FUNCTIONAL

    def tap(self, name, fn, before=True, after=True):
        """
        Creates a :class:`FunctionalTap` for this hook

        Args:
            name (str): Name of the tap
            fn (Callable): This will be called when the hook triggers
            before (bool): If true, this tap will be called *before* the hooked function executes
            after (bool): If true, this tap will be called *after* the hooked function executes
        """
        tap = FunctionalTap(
            name=name,
            fn=fn,
            before=before,
            after=after
        )
        tap = self.interceptor.register(tap) if self.interceptor else tap
        self.taps.append(tap)

    def call(self, fn_args, is_before, fn_output=None):
        """
        Triggers all taps installed on this hook.

        Taps receive predefined arguments `(fn_args, fn_output, context)`

        .. code-block:: python

           fn_args = {
             "args": *args,
             "kwargs": **kwargs
           }

           fn_output = Optional[Any]

           context = {
               'hook_type': FunctionalHook.HOOK_TYPE,
               'hook_type_label': self.label,
               'tap_name': tap.name,
               'is_before': is_before
           }

        Args:
            fn_args (dict): The arguments the hooked function was called with. `fn_args: { args: Tuple, kwargs: Dict }`
            is_before (bool): True if the hook is being called after the hooked function has executed
            fn_output (Optional[Any]): The return value of the hooked function if any. None otherwise
        """
        for tap in self.taps:
            if (tap.before and is_before) or (tap.after and not is_before):
                tap.fn(
                    fn_args=fn_args,
                    fn_output=fn_output,
                    context={
                        'hook_type': FunctionalHook.HOOK_TYPE,
                        'hook_type_label': self.label,
                        'tap_name': tap.name,
                        'is_before': is_before
                    }
                )


class HookableMixin(object):
    """
    Mixin which instantiates all the decorated class methods. This is needed for decorated class methods
    """
    def __init__(self, *args, **kwargs):
        super(HookableMixin, self).__init__(*args, **kwargs)
        self.hooks = {}
        klass = type(self)
        for method in map(partial(getattr, klass), dir(klass)):
            if hasattr(method, '_pytapable'):
                hook_config = getattr(method, '_pytapable')
                self.hooks[hook_config.name] = FunctionalHook(
                    interceptor=hook_config.interceptor
                )

    def inherit_hooks(self, hookable_instance):
        """
        Given an instance which extends the :class:`HookableMixin` class, inherits all hooks from it to expose it on
        top level

        References to the inherited hooks are added in the ``self.hooks`` dict

        Args:
            hookable_instance (HookableMixin): Instance from which to inherit hooks
        """
        self.hooks.update(hookable_instance.hooks)


class CreateHook(object):
    """
    Decorator used for creating Hooks on instance methods. It takes in a name and optionally an instance of a
    :class:`HookInterceptor`.

    .. note::
        This decorator doesn't actually create the hook. It just annotates the method. The hooks are created by the
        :class:`HookableMixin` when the class is instantiated
    """
    def __init__(self, name, interceptor=None):
        self.name = name
        self.interceptor = interceptor

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            hook = args[0].hooks[self.name]
            fn_args = {"args": args, "kwargs": kwargs}

            hook.call(fn_args=fn_args, fn_output=None, is_before=True)

            out = fn(*args, **kwargs)

            hook.call(fn_args=fn_args, fn_output=out, is_before=False)

            return out

        hook_config = HookConfig(name=self.name, interceptor=self.interceptor)
        wrapper._pytapable = hook_config
        return wrapper
