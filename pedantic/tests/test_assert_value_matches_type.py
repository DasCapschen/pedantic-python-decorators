import unittest
from dataclasses import dataclass
from typing import Callable, Awaitable, Coroutine, Any

from pedantic.exceptions import PedanticTypeCheckException
from pedantic.type_checking_logic.check_types import assert_value_matches_type


@dataclass
class Foo:
    value: int


class TestAssertValueMatchesType(unittest.TestCase):
    def test_callable(self):
        def _cb(foo: Foo) -> str:
            return str(foo.value)

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., str],
            err='',
            type_vars={},
        )

        with self.assertRaises(expected_exception=PedanticTypeCheckException):
            assert_value_matches_type(
                value=_cb,
                type_=Callable[..., int],
                err='',
                type_vars={},
            )

    def test_callable_return_type_none(self):
        def _cb(foo: Foo) -> None:
            return print(foo)

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., None],
            err='',
            type_vars={},
        )

    def test_callable_awaitable(self):
        async def _cb(foo: Foo) -> str:
            return str(foo.value)

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., Awaitable[str]],
            err='',
            type_vars={},
        )

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., Awaitable[Any]],
            err='',
            type_vars={},
        )

        with self.assertRaises(expected_exception=PedanticTypeCheckException):
            assert_value_matches_type(
                value=_cb,
                type_=Callable[..., Awaitable[int]],
                err='',
                type_vars={},
            )

        with self.assertRaises(expected_exception=PedanticTypeCheckException):
            assert_value_matches_type(
                value=_cb,
                type_=Callable[..., str],
                err='',
                type_vars={},
            )

    def test_callable_coroutine(self):
        async def _cb(foo: Foo) -> str:
            return str(foo.value)

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., Coroutine[None, None, str]],
            err='',
            type_vars={},
        )

        with self.assertRaises(expected_exception=PedanticTypeCheckException):
            assert_value_matches_type(
                value=_cb,
                type_=Callable[..., Coroutine[None, None, int]],
                err='',
                type_vars={},
            )

    def test_callable_awaitable_with_none_return_type(self):
        async def _cb(foo: Foo) -> None:
            print(foo)

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., Awaitable[None]],
            err='',
            type_vars={},
        )

        assert_value_matches_type(
            value=_cb,
            type_=Callable[..., Awaitable[Any]],
            err='',
            type_vars={},
        )
