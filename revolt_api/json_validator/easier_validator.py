"""
Clearer api for json_validator
"""

from __future__ import annotations

from .validator import StringValidator, IntValidator, ArrayValidator, LITERAL_TYPES, FormattedDict, FormattedList,\
    FloatValidator, UnionValidator, BaseValidator as _BaseValidator


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


_Factory = FlagFactory


Int = _Factory["int"]
Float = _Factory["float"]
Array = _Factory["array"]
OptionalDictElement = _Factory["dict_optional_element"]


def convert(value):
    def convert_with_correct(data):
        if isinstance(data, _BaseValidator):
            return data
        elif isinstance(data, dict):
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

        raise ValueError(f"invalid 'data' argument: {data}")

    def convert_flag(data: Flag):
        if data.tag == "int":
            if len(data.configs) > 0:
                return convert_int(data.configs)
            else:
                return int
        elif data.tag == "float":
            if len(data.configs) > 0:
                return convert_float(data.configs)
            else:
                return float
        elif data.tag == "array":
            return convert_array(data)

    def convert_dict(data: dict):
        optionals = []
        dict_keys_values = []
        for key in data:
            optional_key = False
            d_val = data[key]

            if isinstance(key, Flag):
                if key.tag == "dict_optional_element":
                    optionals.append(key.data)
                    optional_key = True

                key = key.data

            if isinstance(d_val, Flag):
                if d_val.tag == "dict_optional_element":
                    if not optional_key:
                        optionals.append(key)
                    d_val = d_val.data

            dict_keys_values.append((key, convert_with_correct(d_val)))

        dct_settings = (*dict_keys_values, optionals)

        return FormattedDict[dct_settings]

    def convert_list(data: list):
        lst = []
        for el in data:
            lst.append(convert_with_correct(el))
        return FormattedList[tuple(lst)]

    def convert_array(data: Flag):
        return ArrayValidator[convert_with_correct(data.data)]

    def convert_string(data: str):
        return StringValidator[data]

    def convert_int(data: tuple[int, ...]):
        return IntValidator[data]

    def convert_float(data: tuple[int, ...]):
        return FloatValidator[data]

    def convert_bool(data: bool):
        return type(data)

    return convert_with_correct(value)


def union(t1, t2, *a):
    u_lst = [convert(t1), convert(t2)]

    for el in a:
        u_lst.append(convert(el))

    return UnionValidator[tuple(u_lst)]


__all__ = [
    "convert",
    "union",
    "Int",
    "Float",
    "Array",
    "OptionalDictElement"
]
