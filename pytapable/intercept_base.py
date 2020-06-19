

class HookInterceptor(object):
    """
    Interceptors allow you to intercept actions that are being performed on hooks and optionally modify it
    """

    def register(self, context, tap):
        """
        Triggered for each added tap and allows you to modify the tap

        .. code-block:: python

           context = {
             'hook': BaseHook,  # The hook that's being tapped
           }

        Args:
            context (dict)
            tap (Tap): The Tap that is going to be installed on the hook

        Returns:
            modified_tap (Tap): The Tap to install on the hook
        """
        return tap

