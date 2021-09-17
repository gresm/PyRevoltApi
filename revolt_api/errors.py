"""
Module with base revolt_api error
and decorator that that handles exceptions from calling
object method and re-raises it as ApiException
"""

from __future__ import annotations

from types import FunctionType

__all__ = [
    "ApiException",
    "api_error"
]

from typing import Any


class ApiException(Exception):
    pass


class _None:
    pass


class _ApiErrorHandler:
    def __init__(self, fallback: FunctionType | None = None, cause: str = ""):
        self.fallback = fallback
        self.func: FunctionType | None = None
        self.cause = cause
        self._first_call = True
        self._passing_types = (_UnboundErrorHandler, _BoundErrorHandler)

    def __get__(self, instance, owner):
        if isinstance(instance, self._passing_types) or owner in self._passing_types:
            return self
        elif instance is None:
            return self.func
        else:
            return _BoundErrorHandler(self, instance, owner)

    def __call__(self, func: FunctionType | Any = _None, *args, **kwargs):
        if self._first_call:
            self._first_call = False
            self.func = func
            return self

        if func is _None:
            return self._get_unbound_error_handler()(*args, **kwargs)
        else:
            return self._get_unbound_error_handler()(func, *args, **kwargs)

    def _get_unbound_error_handler(self):
        return _UnboundErrorHandler(self)


class _UnboundErrorHandler:
    def __init__(self, ref: _ApiErrorHandler):
        self.ref = ref

    def __call__(self, *args, **kwargs):
        if self.ref.func is None:
            raise ValueError("Function not bound")

        func = self.ref.func
        if self.ref.fallback:
            fallback = self.ref.fallback
        else:
            fallback = None

        try:
            return func(*args, **kwargs)
        except Exception as e:
            if fallback:
                fallback()
            raise ApiException(self._get_error_message(e)) from e

    def _get_error_message(self, e: Exception):
        if isinstance(e, Exception):
            if self.ref.cause:
                return f"exception '{type(e).__name__}: {e}' with message: '{self.ref.cause}'"
            else:
                return f"exception: '{type(e).__name__}: {e}'"
        else:
            if self.ref.cause:
                return f"exception: '{e}' with message: '{self.ref.cause}'"
            else:
                return f"exception: '{e}'"


class _BoundErrorHandler:
    def __init__(self, ref: _ApiErrorHandler, bound_object: object = None, bound_class: type = None):
        self.ref = ref
        self.bound_object = bound_object
        self.bound_class = bound_class

    def __call__(self, *args, **kwargs):
        if self.ref.func is None:
            raise ValueError("Function not bound")

        func = self.ref.func.__get__(self.bound_object, self.bound_class)
        if self.ref.fallback:
            fallback = self.ref.fallback.__get__(self.bound_object, self.bound_class)
        else:
            fallback = None

        try:
            return func(*args, **kwargs)
        except Exception as e:
            if fallback:
                fallback()
            raise ApiException(self._get_error_message(e)) from e

    def _get_error_message(self, e: Exception):
        if isinstance(e, Exception):
            if self.ref.cause:
                return f"exception '{type(e).__name__}: {e}' with message: '{self.ref.cause}'"
            else:
                return f"exception: '{type(e).__name__}: {e}'"
        else:
            if self.ref.cause:
                return f"exception: '{e}' with message: '{self.ref.cause}'"
            else:
                return f"exception: '{e}'"


api_error = _ApiErrorHandler
