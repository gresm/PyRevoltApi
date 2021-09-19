"""
Clearer api for json_validator
"""

from __future__ import annotations

from .validator import *


class FlagFactory:
    def __init__(self, flag_tag: str):
        self.flag_tag = flag_tag

    def __rlshift__(self, other):
        return self.generate_flag(other)

    def __class_getitem__(cls, item):
        return cls(item)

    def __call__(self, *args):
        return self.generate_flag(configs=args)(*args)

    def _get_raw_flag(self, sub_tags: list[str], data, configs: tuple):
        return Flag(self, sub_tags, data, configs)

    def generate_flag(self, data=None, configs=()):
        flags = None
        if isinstance(data, Flag):
            flags = data.tags
            data = data.data
            configs = data.configs

        return self._get_raw_flag(flags if flags is not None else [], data, configs)


_FLAG_TAGS = ArrayValidator[str]


class Flag:
    def __init__(self, factory: FlagFactory, sub_tags: list[str], data, configs: tuple,
                 no_factory_tag: bool = False):
        self._factory = factory
        self.data = data
        self.tag = self._factory.flag_tag
        self._sub_tags = sub_tags
        if no_factory_tag:
            self.tags = self._sub_tags
        else:
            self.tags = self._sub_tags + [self.tag]

        self.configs = configs if configs is not None else ()

    def __hash__(self):
        return hash(id(self))

    def __call__(self, *data):
        return self.new_configs(data)

    def __rlshift__(self, other):
        return self.generate_flag(other)

    def new_configs(self, configs: tuple):
        return self.__class__(self._factory, self.tags, self.data, configs, True)

    def generate_flag(self, data):
        self.data = data
        return self


def convert(value):
    def convert_with_correct(data):
        if isinstance(data, dict):
            return convert_dict(data)
        elif isinstance(data, list):
            return convert_list(data)
        elif isinstance(data, tuple):
            return convert_list(list(data))
        elif isinstance(data, str):
            return convert_string(data)
        elif isinstance(data, int):
            return int
        elif isinstance(data, float):
            return float
        elif isinstance(data, bool):
            return convert_bool(data)
        elif isinstance(data, LITERAL_TYPES):
            return data
        elif isinstance(data, Flag):
            return convert_flag(data)

    def convert_flag(data: Flag):
        pass

    def convert_dict(data: dict):
        pass

    def convert_list(data: list):
        pass

    def convert_array(data):
        pass

    def convert_string(data: str):
        return StringValidator[data]

    def convert_int(data: tuple[int, ...]):
        pass

    def convert_float(data: tuple[int, ...]):
        pass

    def convert_bool(data: bool):
        return type(data)

    return convert_with_correct(value)
