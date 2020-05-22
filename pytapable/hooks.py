import uuid
from collections import namedtuple

from .intercept_base import HookInterceptor

HookConfig = namedtuple('HookConfig', ['name', 'interceptor'])


class Tap(object):
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn


class BaseHook(object):
    HOOK_TYPE = -1

    FUNCTIONAL, INLINE = range(2)  # hook types

    HOOK_TYPE_LABEL = {
        FUNCTIONAL: 'Function',
        INLINE: 'Inline'
    }

    def __init__(self, interceptor: HookInterceptor = None):
        self.taps = []
        self.interceptor = interceptor

    def tap(self, *args, **kwargs):
        pass

    def call_taps(self, *args, **kwargs):
        pass

    def intercept(self, interceptor):
        self.interceptor = interceptor

    @property
    def label(self):
        return self.HOOK_TYPE_LABEL[self.HOOK_TYPE]


def create_hook_name(name):
    prefix = str(uuid.uuid4())
    return "{}:{}".format(prefix, name)
