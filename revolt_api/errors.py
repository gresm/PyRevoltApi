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


class ApiException(Exception):
    pass


class _ApiErrorHandler:
    def __init__(self, fallback: FunctionType | None = None):
        self.fallback = fallback
        self.func: FunctionType | None = None

    def __get__(self, instance, owner):
        if isinstance(instance, _BoundErrorHandler) or owner is _BoundErrorHandler:
            return self
        elif instance is None:
            return self.func
        else:
            return _BoundErrorHandler(self, instance, owner)

    def __call__(self, func: FunctionType):
        if self.func is None:
            self.func = func
            return self
        else:
            return func


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
            raise ApiException(e) from e


api_error = _ApiErrorHandler
