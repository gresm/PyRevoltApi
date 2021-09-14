from __future__ import annotations
from threading import Thread
from typing import Any

import requests as rq


__all__ = [
    "RequestError",
    "RequestThread"
]


class RequestError(Exception):
    pass


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
        return self.result

    def run(self) -> None:
        self.running = True
        try:
            self.result = rq.request(
                self.method, self.url,
                params=self.params, data=self.data,
                headers=self.headers, json=self.json
            )
        except rq.RequestException as e:
            self.failed = True
            raise RequestError(e)
        finally:
            self.running = False

    def response_json(self):
        try:
            return self.result.json()
        except Exception as e:
            raise RequestError(e)
