from pytapable import BaseHook, HookableMixin


class Car(HookableMixin):

    def __init__(self):
        super(Car, self).__init__()
        self.hooks['on_move'] = BaseHook()

    def move(self):
        self.hooks['on_move'].call_taps(first_name='vidhu', age=26)
        return "move"


def callback(**kwargs):
    print(kwargs)


c = Car()
c.hooks['on_move'].tap('my_tap', callback)
c.move()



