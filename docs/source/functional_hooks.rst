.. py:currentmodule:: pytapable

Functional Hooks
****************

Functional hooks are hooks which wrap a function. They fire before and after the execution of a function automatically.

They are created using decorators on the function.

Useage on Class Instance methods
--------------------------------

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

When a method is decorated using the ``@CreateHook`` decorator, the wrapped function is marked. The class must extend the
``HookableMixin`` class. This is necessary because when the ``Car`` class is initialized, the hookable mixin goes through
all the marked methods and constructs a ``FunctionalHook`` for each of them.

These newly created hooks are stored on the ``instance.hooks`` attribute which is defined by the ``HookableMixin`` class

Arguments passed to callables from a FunctionalHook are predefined unlike InlineHooks. Refer to the documentation below
to understand the arguments


API Documentation
-----------------

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
   :members: inherit_hooks

create_hook_name
^^^^^^^^^^^^^^^^
.. autofunction:: create_hook_name

create_hook_names
^^^^^^^^^^^^^^^^^
.. autofunction:: create_hook_names


