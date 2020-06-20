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

    default_arg_value = zip(reversed(argspec.args), reversed(argspec.defaults or ()))

    # Apply defaults if values are missing
    for arg_name, arg_val in default_arg_value:
        if arg_name not in fn_args_to_kwargs:
            fn_args_to_kwargs[arg_name] = arg_val

    if argspec.varargs and len(args) > len(argspec.args):
        # We were given more args than possible so they much be part of *args
        fn_args_to_kwargs['*{}'.format(argspec.varargs)] = args[len(argspec.args)-len(args):]

    return fn_args_to_kwargs
