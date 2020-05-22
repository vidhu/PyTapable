from pytapable import CreateHook, HookableMixin
from functools import partial


class MyClass(HookableMixin):
    HOOK_MOVE, = range(1)

    @property
    @CreateHook(HOOK_MOVE)
    def move(self):
        return "I moved"


class MyParentClass(HookableMixin):
    HOOK_SAY, = range(1)

    def __init__(self):
        super(MyParentClass, self).__init__()
        self.inherit_hooks(self.my_class)

    @property
    def my_class(self):
        return MyClass()

    @CreateHook(HOOK_SAY)
    def say(self):
        print(self.my_class.move)
        return "I said"


my_class_1 = MyClass()


my_parent_class = MyParentClass()
my_parent_class.hooks[MyClass.HOOK_MOVE].tap('my tap 1', partial(print, 'move Hook!'))
my_parent_class.hooks[MyParentClass.HOOK_SAY].tap('my tap 1', partial(print, 'say Hook!'))
my_parent_class.say()


