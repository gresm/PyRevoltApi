from .errors import *
from . import errors
from . import rest_api

base_url = "https://api.revolt.com/"


def set_url(url: str):
    global base_url
    base_url = url


def get_url():
    return base_url


__all__ = [
    "set_url",
    "get_url",
    "rest_api",
    *errors.__all__
]
