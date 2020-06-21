Interceptors
============

Interceptors can be thought of as hooks for your hooks.

.. code-block:: python

   from pytapable import Hook, HookInterceptor


   class TapLogger(HookInterceptor):

       def create(self, hook):
           print(f"Hook {hook.name} initialized")

       def register(self, context, tap):
           print(f"Hook being tapping is '${context['hook']}'")
           print(f"Hook being tapped by '${tap.name}'")
           return tap

   tap_logger = TapLogger()

   my_hook = Hook(interceptor=tap_logger)

   >>> Hook XYZ initialized


   my_hook.tap('My Tap', my_callback)

   >>> Hook being tapped by 'My Tap'


They are a mechanism for you to intercept whenever one of your hooks are tapped into or when a hook was created

The return value of the ``register`` method must be a tap. If you need to modify the behavior of the callback in the
tap, this is the place to do it.


API Documentation
=================

HookInterceptor
---------------

.. autoclass:: pytapable.HookInterceptor
   :members:

Tap
---

.. autoclass:: pytapable.Tap
   :members:

