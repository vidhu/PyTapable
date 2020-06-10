Recipies
********

Here's a list of interesting ways to use hooks. If you find an interesting way to use hooks that's worthy of sharing,
please contribute by making a pull request!

Timing how long taps take
=========================

We don't always know what is tapping our hooks. This might make monitoring challenging especially if there are SLOs to
be met.

Here we wrap callbacks in statsd timers using an interceptor and log them against a key derived from the stats' name

.. code-block:: python

   class InterceptorHookTimer(HookInterceptor):

       def register(self, tap):
           tap.fn = statsd.timer(f"interceptor.${tap.name}")(tap.fn)
           return tap