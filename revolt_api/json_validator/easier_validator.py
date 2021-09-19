"""
Clearer api for json_validator
"""

from __future__ import annotations

from .validator import *


class FlagFactory:
    def __init__(self, flag_tag: str, configs: tuple = None):
        self.flag_tag = flag_tag
        self.configs = configs if configs is not None else []

    def __call__(self, *data):
        return self.new_configs(data)

    def __rlshift__(self, other):
        return self.generate_flag(other)

    def __class_getitem__(cls, item):
        return cls(item)

    def _get_raw_flag(self, sub_tags: list[str], data):
        return Flag(self, sub_tags, data)

    def generate_flag(self, data):
        flags = None
        if isinstance(data, Flag):
            flags = data.tags
            data = data.data

        return self._get_raw_flag(flags if flags is not None else [], data)

    def new_configs(self, configs: tuple):
        return self.__class__(self.flag_tag, configs)


_FLAG_TAGS = ArrayValidator[str]


class Flag:
    def __init__(self, factory: FlagFactory, sub_tags: list[str], data):
        self._factory = factory
        self.data = data
        self.tag = self._factory.flag_tag
        self._sub_tags = sub_tags
        self.tags = self._sub_tags + [self.tag]

    def __hash__(self):
        return hash(id(self))


def convert(value):
    def convert_with_correct(data):
        if isinstance(data, dict):
            return convert_dict(data)
        elif isinstance(data, list):
            return convert_list(data)
        elif isinstance(data, str):
            return convert_string(data)
        elif isinstance(data, int):
            return convert_int(data)
        elif isinstance(data, float):
            return convert_float(data)
        elif isinstance(data, bool):
            return convert_bool(data)
        elif isinstance(data, LITERAL_TYPES):
            return data

    def convert_dict(data):
        pass

    def convert_list(data):
        pass

    def convert_array(data):
        pass

    def convert_string(data):
        pass

    def convert_int(data):
        pass

    def convert_float(data):
        pass

    def convert_bool(data):
        return type(data)

    return convert_with_correct(value)
