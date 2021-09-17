from __future__ import annotations

from . import RequestThread, convert_url
from .. import api_error

import ulid

__all__ = [
    "ValidatedRequest"
]


class ValidatedRequest:
    def __init__(self, validation_token: str, is_bot: bool, url: str = "https://api.revolt.chat/", method: str = "GET"):
        self.validation_token = validation_token
        self.is_bot = is_bot
        self.base_url = url
        self.method = method
        self.request_ref: RequestThread | None = None

    @property
    def headers(self):
        if self.is_bot:
            return {"x-bot-token": self.validation_token}
        else:
            return {"x-session-token": self.validation_token}

    @headers.setter
    def headers(self, value):
        pass

    @property
    def response(self):
        return self.request_ref.result if self.request_ref is not None else None

    @api_error(cause="Invalid arguments: json not passed or data is not valid json string")
    def _add_nonce(self, dct: dict | None, with_ulid: bool = False, pos: str = "nonce"):
        print("fixing")

        if not with_ulid:
            return dct

        dct[pos] = ulid.ulid()
        return dct

    def request(self, json: dict | None = None, data: str = "", params: dict[str, str] = None, url: str = "",
                method: str = "GET", path_args: tuple[str] = (), path_kwargs: dict[str, str] = None,
                with_ulid: bool = False, *args, **kwargs):
        if path_kwargs is None:
            path_kwargs = {}

        json = self._add_nonce(json, with_ulid)

        url = convert_url(url, self.base_url, url_args=path_args, url_kwargs=path_kwargs, *args, **kwargs)
        return self._run_request_thread(url, method, params, data, json)

    def _run_request_thread(self, url: str, method: str, params: dict[str, str], data: str, json):
        self.request_ref = RequestThread(url, method, self.headers, params, data, json)
        self.request_ref.start()
        return self.request_ref
