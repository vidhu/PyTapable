import uuid
from typing import Iterable
from collections import namedtuple

HookConfig = namedtuple('HookConfig', ['name', 'interceptor'])


class Tap(object):
    """
    A Tap is an object created when you tap into a hook. It holds a reference to the function you want to
    execute when the hook triggers
    """
    def __init__(self, name, fn):
        """

        Args:
            name (str): Name of the tap
            fn (Callable): This will be called when the hook triggers
        """
        self.name = name
        self.fn = fn


class BaseHook(object):
    HOOK_TYPE = -1

    FUNCTIONAL, INLINE = range(2)  # hook types

    HOOK_TYPE_LABEL = {
        FUNCTIONAL: 'Function',
        INLINE: 'Inline'
    }

    def __init__(self, interceptor=None):
        self.taps = []
        self.interceptor = interceptor

    def tap(self, *args, **kwargs):
        pass

    def call(self, *args, **kwargs):
        pass

    def intercept(self, interceptor):
        self.interceptor = interceptor

    @property
    def label(self):
        return self.HOOK_TYPE_LABEL[self.HOOK_TYPE]


def create_hook_name(name=""):
    """
    Utility to create a unique hook name. Optionally takes in a name. The output string is the name prefixed with a
    UUID. This is useful to prevent collision in hook names when one class with hooks inherits hooks from another class

    Example:
        >>> create_hook_name()
        >>> '7087eefc-8e94-4f0a-b7d3-453062bb7a34'
        >>> create_hook_name('my_hook')
        >>> '7087eefc-8e94-4f0a-b7d3-453062bb7a34:my_hook'

    Args:
        name (Optional[str]): Name of the hook
    """
    prefix = str(uuid.uuid4())
    return "{}:{}".format(prefix, name)


def create_hook_names(*names):
    """
    Useful shortcut to create multiple unique hook names in one statement

    Example:
        >>> HOOK_MY, HOOK_UNIQUE, HOOK_HOOK = create_hook_names('my', 'unique', 'hook')
        >>> HOOK_ONE, HOOK_TWO, HOOK_THREE = create_hook_names(*range(3))

    Args:
        \*names: Argument of hook names
    Returns:
        Iterable: iterable which can be deconstructed across constants.
    """

    for name in names:
        yield create_hook_name(name)
