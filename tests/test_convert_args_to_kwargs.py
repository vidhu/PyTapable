from unittest import TestCase

import inspect

from pytapable.utils import merge_args_to_kwargs


class TestOnlyArgs(TestCase):

    def test_only_args(self):
        def fn(a, b):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(1, 2),
            kwargs={}
        )

        assert kwargs == {
            'a': 1,
            'b': 2
        }

    def test_only_args_with_extra_arg(self):
        def fn(a, *args):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(1, 2),
            kwargs={}
        )

        assert kwargs == {
            'a': 1,
            '*args': (2,)
        }

    def test_only_args_with_default_arg(self):
        def fn(a, b=2, c=3):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=('A',),
            kwargs={}
        )

        assert kwargs == {
            'a': 'A',
            'b': 2,
            'c': 3
        }

    def test_only_args_with_extra(self):
        def fn(a, b, *args):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(1, 2, 3, 4, 5),
            kwargs={}
        )

        assert kwargs == {
            'a': 1,
            'b': 2,
            '*args': (3, 4, 5)
        }


class TestOnlyKwargs(TestCase):

    def test_only_kwargs(self):
        def fn(a, b):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(),
            kwargs={'a': 1, 'b': 2}
        )

        assert kwargs == {
            'a': 1,
            'b': 2
        }

    def test_only_kwargs_with_extra_arg(self):
        def fn(a, *kwargs):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(),
            kwargs={'a': 1, 'b': 2}
        )

        assert kwargs == {
            'a': 1,
            'b': 2
        }

    def test_only_kwargs_with_default_arg_in_order(self):
        def fn(a, b=2, c='2345'):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(),
            kwargs={'a': 1}
        )

        assert kwargs == {
            'a': 1,
            'b': 2,
            'c': '2345'
        }

    def test_only_kwargs_with_default_arg_out_of_order(self):
        def fn(a, b=2, c=3):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=(),
            kwargs={'a': 'A', 'c': 'C'}
        )

        assert kwargs == {
            'a': 'A',
            'b': 2,
            'c': 'C'
        }


class TestMixed(TestCase):

    def test_args_and_kwargs(self):
        def fn(a, b=2, c=3):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=('A',),
            kwargs={'b': 'B', 'c': 'C'}
        )

        assert kwargs == {
            'a': 'A',
            'b': 'B',
            'c': 'C'
        }

    def test_args_and_kwargs_with_default(self):
        def fn(a, b=2, c=3):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=('A',),
            kwargs={'c': 'C'}
        )

        assert kwargs == {
            'a': 'A',
            'b': 2,
            'c': 'C'
        }

    def test_args_and_kwargs_with_extra_and_default(self):
        def fn(a, b=2, c=3, *args, **kwargs):
            pass

        kwargs = merge_args_to_kwargs(
            argspec=inspect.getfullargspec(fn),
            args=('A', 'B', 'C', 'D'),
            kwargs={'e': 'E'}
        )

        assert kwargs == {
            'a': 'A',
            'b': 'B',
            'c': 'C',
            'e': 'E',
            '*args': ('D',)
        }