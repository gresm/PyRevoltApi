"""
Clearer api for json_validator
"""

from __future__ import annotations

from validator import *


class Element:
    def __init__(self, val):
        self.val = val
        self.flags = None
        self.has_flags = False


class FlagFactory:
    def __init__(self, flag_tag: str):
        self.flag_tag = flag_tag

    def __call__(self, data):
        pass

    def _get_raw_flag(self, sub_tags: list[str], data):
        return Flag(self, sub_tags, data)

    def generate_flag(self, data):
        flags = None
        if isinstance(data, Flag):
            flags = data.tags

        return self._get_raw_flag(flags if flags is not None else [], data)


_FLAG_TAGS = ArrayValidator[str]


class Flag:
    def __init__(self, factory: FlagFactory, sub_tags: list[str], data):
        self._factory = factory
        self.data = data
        self.tag = self._factory.flag_tag
        self._sub_tags = sub_tags
        self.tags = self._sub_tags + list(self.tag)
