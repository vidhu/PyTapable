from unittest import TestCase
from pytapable.utils import merge_args_to_kwargs, get_arg_spec_py2_py3


class TestMixedPy3(TestCase):

    def test_pep3102_ignore_args(self):
        def fn(a, b, *, d):  # noqa: E999
            pass

        kwargs = merge_args_to_kwargs(
            argspec=get_arg_spec_py2_py3(fn),
            args=('A', 'B', 'C1', 'C2'),
            kwargs={'d': 'D'}
        )

        assert kwargs == {
            'a': 'A',
            'b': 'B',
            'd': 'D'
        }
