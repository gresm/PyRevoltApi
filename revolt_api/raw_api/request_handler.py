from __future__ import annotations
from threading import Thread
from typing import Any
from types import FunctionType

import requests as rq


from .. import api_error


__all__ = [
    "RequestThread"
]


class RequestThread(Thread):
    def __init__(self, url: str, method: str = "GET", headers: dict[str, str] = None, params: dict[str, str] = None,
                 data: str = "", json: Any | None = None):
        super().__init__()
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json
        self.running = False
        self.finished = False
        self.result: rq.Response | None = None
        self.failed = False

    def request(self, json: Any | None = None, data: str = "",  params: dict[str, str] = None):
        self.params = params
        self.data = data
        self.json = json
        self.start()

    def fail(self):
        self.failed = True
        self.running = False

    fail: FunctionType

    @api_error(fail)
    def run(self) -> None:
        self.running = True
        self.result = rq.request(
            self.method, self.url,
            params=self.params, data=self.data,
            headers=self.headers, json=self.json
        )

    @api_error()
    def response_json(self):
        return self.result.json()
