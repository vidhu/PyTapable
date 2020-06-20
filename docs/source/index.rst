PyTapable Documentation
=======================

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Contents:

   inline_hooks
   functional_hooks
   interceptors
   recipes
   contributing

.. image:: https://github.com/vidhu/PyTapable/workflows/Tests/badge.svg
   :target: https://github.com/vidhu/PyTapable/actions?query=branch%3Amaster+event%3Apus
   :alt: Test Status

.. image:: https://img.shields.io/pypi/v/PyTapable
   :target: https://pypi.org/project/PyTapable/
   :alt: PyPi

.. image:: https://img.shields.io/codecov/c/github/vidhu/PyTapable
   :target: https://img.shields.io/codecov/c/github/vidhu/PyTapable
   :alt: Code Coverage

.. image:: https://img.shields.io/pypi/pyversions/PyTapable
   :target: https://pypi.org/project/PyTapable/#history
   :alt: Python Versions

.. image:: https://api.codeclimate.com/v1/badges/f26988bb91b39a67c08e/maintainability
   :target: https://codeclimate.com/github/vidhu/PyTapable/maintainability
   :alt: Maintainability and Code Quality

.. image:: https://img.shields.io/pypi/dd/PyTapable
   :target: https://pypi.org/project/PyTapable/
   :alt: Downloads a day

.. image:: https://img.shields.io/pypi/l/pytapable
   :target: https://github.com/vidhu/PyTapable/blob/master/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/Maintained-yes-green.svg
   :alt: Maintained


Installation
------------
.. code-block:: bash

   $ pip install pytapable

Introduction
------------
PyTapable provides a way to attach hooks into your application. Its a way to implement event listeners with
side effects. This is particularly useful to maintain service boundaries in your application, allow plugable in
your libraries which you users can extend upon etc


Lets first clarify the terminologies used in this library

.. glossary::

   Hook
      A Hook is an object which maintains a list of taps that have been installed/registered with it

   Tap
      A Tap is an object which holds a reference to the function which is to be run when a hook is *executed*.

   tapping
      Tapping into a hook is the act of registering a callable with a hook

   callbacks
      Consumer defined function/callable which is executed in response to a hook being triggered

Type of Hooks
^^^^^^^^^^^^^

There are two types of hooks provided in this library

 - **FunctionalHook:** Functional hooks are hooks which wrap a function. They fire before and after the execution of a
   function automatically. They are created using decorators on the function. See :doc:`functional_hooks`
 - **InlineHook:** Inline hooks are created and triggered manually. They are used in the body of functions and modules
   See :doc:`inline_hooks`

The parameters your :term:`callbacks` are called with differ based on which hooks there were called
from. Callbacks from a functional hook contain the function's arguments and return value (if available) whereas
callbacks from an inline hook contain parameters defined by the caller

Context
^^^^^^^

A context dict is also passed to the callback function which contain various metadata. This is covered in more detail
in the API doc for :ref:`FunctionalHook` and :ref:`Hook`

Quick Start
-----------
Here's an example on how to use `InlineHooks` and `FunctionalHooks`

InlineHooks
^^^^^^^^^^^
.. code-block:: python

   from pytapable import Hook

   # 1. Create our hook
   my_hook = Hook()

   # 2. Define a function to execute when hook triggers
   def my_callback(context, fn_kwargs):
      print(f"Hook says: {fn_kwargs['greeting']}")

   # 3. Tap into our hook
   my_hook.tap('My Tap Name', my_callback)

   # 4. Trigger our hook
   my_hook.call(greeting="Hi Callback")

   >>> "Hook says: Hi Callback"



FunctionalHooks
^^^^^^^^^^^^^^^
Lets define out class with a hookable instance method

.. code-block:: python

   from pytapable import CreateHook, HookableMixin, create_hook_name

   # 1. Class extends `HookableMixin` to initialize hooks on instance
   class Car(HookableMixin):
      HOOK_ON_MOVE = create_hook_name('on_move')

      # 2. Mark this method as hookable
      @CreateHook(name=HOOK_ON_MOVE)
      def move(self, speed=10):
         return f"Moving at {speed}Mph"


and then tap into the hook

.. code-block:: python

   def log_metric_speed(context, fn_kwargs, fn_output):
      kmph_speed = fn_kwargs['speed'] * 1.61
      print(f"The car is moving at {kmph_speed} kmph")

   c = Car()

   # 3. Tap into our hook. before=False means callback will
   #    execute after hooked function returns
   c.hooks[Car.HOOK_ON_MOVE].tap(
      'log_metric_speed',
      log_metric_speed,
      before=False
   )

   # 4. Hook is automatically triggered
   c.move(speed=10)

   # Positional args are converted to named arguments
   c.move(10)

   >>> "The car is moving at 16.1 kmph"

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
