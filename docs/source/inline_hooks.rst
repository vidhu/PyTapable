Inline Hooks
============

Inline hooks are defined inline with business logic code. They are manually triggered with user defined arguments which
are received by callback functions

Usage
-----

Inline
^^^^^^

.. code-block:: python

   from pytapable import Hook

   # 1. Create our hook
   my_hook = Hook()

   # 2. Define a function to execute when hook triggers
   def my_callback(context, greeting):
      print(f"Hook says: {greeting}")

   # 3. Tap into our hook
   my_hook.tap('My Tap Name', my_callback)

   # 4. Trigger our hook
   my_hook.call(greeting="Hi Callback")

   >>> "Hook says: Hi Callback"

In a Class
^^^^^^^^^^

.. code-block:: python
   :emphasize-lines: 4-5,11,15

   from pytapable import HookableMixin, create_hook_name

   # 1. Class extends `HookableMixin`
   class Car(HookableMixin):
      HOOK_ON_MOVE = create_hook_name('on_move')

      def __init__(self):
         super(Car, self).__init__()

         # 2. Define the hook
         self.hooks[HOOK_ON_MOVE] = Hook()

      def move(self, speed=10):
         # 3. Trigger the hook
         self.hooks[HOOK_ON_MOVE].call(speed=speed)
         return f"Moving at {speed}Mph"


.. note::
   When using inline hooks in a class, its useful to have the class extend the :class:`HookableMixin` class and
   create the hooks in the ``self.hooks`` dictionary. This allows inheriting hooks.


Inline Hooks Documentation
--------------------------

Hook
^^^^

.. autoclass:: pytapable.Hook
   :members:
   :inherited-members:

HookableMixin
^^^^^^^^^^^^^
.. autoclass:: pytapable.HookableMixin
   :noindex:
   :members: inherit_hooks
