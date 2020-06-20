from inspect import FullArgSpec


def merge_args_to_kwargs(argspec, args, kwargs):
    """
    Based on the argspec, converts args to kwargs and merges them into kwargs

    Note:
        This returns a new dict instead of modifying the kwargs in place

    Args:
        argspec (FullArgSpec): output from `inspect.getfullargspec`
        args (tuple): List of args
        kwargs (dict): dict of names args

    Returns:
        dict: dict of original named are and args that were converted to named agrs
    """
    fn_args_to_kwargs = {arg_name: arg_val for arg_name, arg_val in zip(argspec.args, args)}
    # We create a copy of the dict to keep the original **kwarg dict pristine
    fn_kwargs = kwargs.copy()
    fn_args_to_kwargs.update(fn_kwargs)

    if len(args) > len(argspec.args):
        fn_args_to_kwargs['*{}'.format(argspec.varargs)] = args[len(args) - len(argspec.args):]

    return fn_args_to_kwargs
