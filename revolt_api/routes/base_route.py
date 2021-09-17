from __future__ import annotations

import warnings

from ..raw_api import ValidatedRequest
from .. import get_url


class Route:
    def __init__(self, url: str, method: str, with_auth: bool = True, can_be_bot: bool = True,
                 params: dict[str, str] = None, with_ulid: bool = False):
        self.url = url
        self.method = method
        self.with_auth = with_auth
        self.can_be_bot = can_be_bot
        self.params = params
        self.with_ulid = with_ulid


def run_route(route: Route, token: str = None, json: dict | None = None, as_bot: bool = False,
              url_kwargs: dict[str, str] = None):
    if not route.can_be_bot and as_bot:
        warnings.warn("Function was run with 'as_bot' argument set to True, but current route doesn't allow to run as "
                      "bot.")
        as_bot = False
    ret = ValidatedRequest(
        is_bot=as_bot, with_auth=route.with_auth,
        validation_token=token, url=get_url(),
        method=route.method
    )

    ret.request(
        json=json, data="",
        params=route.params, url=route.url,
        path_kwargs=url_kwargs, with_ulid=route.with_ulid
    )
    return ret


__all__ = [
    "Route",
    "run_route"
]
