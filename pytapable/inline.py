from .hooks import BaseHook, Tap


class Hook(BaseHook):
    HOOK_TYPE = BaseHook.INLINE

    def tap(self, name, fn):
        tap = Tap(name=name, fn=fn)
        tap = self.interceptor.register(tap) if self.interceptor else tap
        self.taps.append(tap)

    def call_taps(self, *args, **kwargs):
        for tap in self.taps:
            tap.fn(*args, **kwargs)
