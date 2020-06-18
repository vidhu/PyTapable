.. py:currentmodule:: pytapable

Functional Hooks
****************

Functional hooks are hooks which wrap a function. They fire before and after the execution of a function automatically.

They are created using decorators on the function.

Usage on Class Instance methods
-------------------------------

.. code-block:: python

   from pytapable import CreateHook, HookableMixin, create_hook_name

   # 1. Class extends `HookableMixin` to initialize hooks on instance
   class Car(HookableMixin):
      HOOK_ON_MOVE = create_hook_name('on_move')

      # 2. Mark this method as hookable
      @CreateHook(name=HOOK_ON_MOVE)
      def move(self, speed=10):
         return f"Moving at {speed}Mph"

   c = Car()
   c.hooks[Car.HOOK_ON_MOVE].tap(
      'log_metric_speed',
      lambda fn_args, fn_output, context: ...,
      before=False
   )

How it works
^^^^^^^^^^^^

When a method is decorated using the :func:`CreateHook` decorator, the wrapped function is marked. The class must extend
the :class:`HookableMixin` class. This is necessary because when the ``Car`` class is initialized, the hookable mixin
goes through all the marked methods and constructs a :class:`FunctionalHook`` for each of them.

These newly created hooks are stored on the ``instance.hooks`` attribute which is defined by the :class:`HookableMixin`
class

Arguments passed to callables from a :class:`FunctionalHook` are predefined unlike :class:`Hook` (inline hook).
Refer to the documentation below to understand the arguments

Inheritance
^^^^^^^^^^^
:class:`HookableMixin` allows you to inherit hooks from other classes that implement the :class:`HookableMixin`

.. code-block:: python
   :emphasize-lines: 7,10

   class MyClass(HookableMixin):

      def __init__(self):
         super(MyClass, self).__init__()
         self.car = Car()

         self.hooks.inherit_hooks(self.car)

   my_class = MyClass()
   my_class.hooks[Car.HOOK_ON_MOVE].tap(...)

Functional Hooks Documentation
------------------------------

FunctionalHook
^^^^^^^^^^^^^^

.. autoclass:: FunctionalHook
   :members: call, tap

CreateHook
^^^^^^^^^^
.. autodecorator:: CreateHook

HookableMixin
^^^^^^^^^^^^^
.. autoclass:: HookableMixin

HookMapping
^^^^^^^^^^^
.. autoclass:: HookMapping
   :members:

create_hook_name
^^^^^^^^^^^^^^^^
.. autofunction:: create_hook_name

create_hook_names
^^^^^^^^^^^^^^^^^
.. autofunction:: create_hook_names


