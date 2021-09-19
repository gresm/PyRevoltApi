from __future__ import annotations

from builtins import getattr
from typing import Union
import re


_VALIDATOR = "NonBaseClassTypeValidator[BaseValidator]"
_STR = str
_INT = int
_FLOAT = float
_BOOL = bool
_NONE = None
_LIST = list
_DICT = dict

_BASE_TYPING = Union[_VALIDATOR, str, int, float, bool, None, list[...], dict[str, ...], type]
_BASE_TYPING = Union[
    _VALIDATOR, str, int, float, bool, None, list[_BASE_TYPING, ...], dict[str, _BASE_TYPING, ...], type
]

_TYPING_WITHOUT_VALIDATOR = Union[str, int, float, bool, None, list[...], dict[str, ...], type]
_TYPING_WITHOUT_VALIDATOR = Union[
    str, int, float, bool, None, list[_TYPING_WITHOUT_VALIDATOR, ...],
    dict[str, _TYPING_WITHOUT_VALIDATOR, ...], type
]

_FLAT_BASE = Union[str, int, float, bool, None, list, dict[str], type]


class BaseValidator:
    checking_type: type = object

    def __class_getitem__(cls, item: tuple[_BASE_TYPING, ...] | _BASE_TYPING):
        ret = cls.__new__(cls)
        ret.__init__(item)
        return ret

    def __init__(self, settings: tuple[_BASE_TYPING, ...] | _BASE_TYPING):
        self.info = {}
        self.settings = settings if isinstance(settings, tuple) else (settings,)
        self.parse_settings()

    def __getattr__(self, item):
        if item in self.info:
            return self.info[item]
        raise AttributeError

    def __instancecheck__(self, instance):
        return self.check_instance(instance)

    def check_instance(self, value):
        return self.check_type(value) and self.validate(value)

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return False

    def parse_settings(self):
        pass

    def check_type(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return isinstance(data, self.checking_type)


class TypeValidator(BaseValidator):
    checking_type = type

    def parse_settings(self):
        assert len(self.settings) == 1, "Give ony one argument."

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return issubclass(data, self.settings[0])


class NonBaseClassTypeValidator(BaseValidator):
    checking_type = object

    def parse_settings(self):
        assert len(self.settings) == 1, "Give ony one argument."

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return isinstance(data, self.settings[0]) and type(data) is not self.settings[0]


_VALIDATOR_CLASS = NonBaseClassTypeValidator[BaseValidator]


class StringValidator(BaseValidator):
    checking_type = str

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        matched = re.fullmatch(self.settings[0], data)
        return matched is not None


class IntValidator(BaseValidator):
    checking_type = int

    def __init__(self, settings: tuple[_BASE_TYPING, ...] | _BASE_TYPING = ()):
        super().__init__(settings)

    def parse_settings(self):
        size = len(self.settings)
        if size >= 1:
            self.info["first"] = self.settings[0]

        if size >= 2:
            self.info["last"] = self.settings[1]

        if size >= 3:
            self.info["steps"] = self.settings[2]

        self.info["mode"] = size

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        if not isinstance(data, int):
            return False

        if self.info["mode"] == 0:
            return True
        elif self.info["mode"] == 1:
            return data >= self.info["first"]
        elif self.info["mode"] == 2:
            return self.info["first"] <= data < self.info["last"]
        elif self.info["mode"] >= 3:
            return self.info["first"] <= data < self.info["last"] and (data - self.info["first"]) % self.info[
                "steps"] == 0


class FloatValidator(IntValidator):
    checking_type = float


class ArrayValidator(BaseValidator):
    """
    It validates list, but every element has to be
    same 'Validator'
    """
    checking_type = list

    def parse_settings(self):
        assert len(self.settings) == 1, "Give ony one argument."
        assert isinstance(self.settings[0], _VALIDATOR_CLASS) is not BaseValidator or \
               isinstance(self.settings[0], type), \
               "Class of the argument has to be an subclass of 'BaseValidator', but not exactly a 'BaseValidator'"
        self.info["check_to"] = self.settings[0]

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        for el in data:
            if not isinstance(el, (self.info["check_to"],)):
                return False
        return True


class ExactListValidator(BaseValidator):
    """
    It validates list with constant length and constant data structure
    """
    checking_type = list

    def parse_settings(self):
        assert len(self.settings) >= 1, "Give at least one argument."
        for el in self.settings:
            assert isinstance(el, BaseValidator) and type(el) is not BaseValidator, \
                "Classes of the arguments shall be an subclasses of 'BaseValidator', but not exactly a 'BaseValidator'"
        self.info["structure"] = self.settings
        self.info["size"] = len(self.settings)

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        if len(data) != self.info["size"]:
            return False

        for ind in range(len(data)):
            if not isinstance(data[ind], self.info["structure"][ind]):
                return False
        return True


class UnionValidator(BaseValidator):
    """
    Union validator checks if validating data is valid for one of the given types.
    """
    checking_type = object

    def parse_settings(self):
        assert len(self.settings) >= 2, "Give at least two arguments."

        fixed = []

        for el in self.settings:
            if el is None:
                # for none
                fixed.append(type(el))
            elif isinstance(el, (type, BaseValidator)) and type(el) is not BaseValidator:
                # for types + for Validators
                fixed.append(el)
            elif getattr(el, "__instancecheck__", None) is not None:
                # for custom type checking
                fixed.append(el)
            else:
                raise ValueError("Arguments shall be types or None or Validators or at least define "
                                 "'__instancecheck__'")

        self.info["fixed"] = tuple(fixed)

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return isinstance(data, (self.info["fixed"]), )


LITERALS = UnionValidator[str, int, float, bool, None]
LITERAL_TYPES = UnionValidator[TypeValidator[str], TypeValidator[int], TypeValidator[float], TypeValidator[bool]]
CHECKING_OBJECTS = UnionValidator[LITERALS, list, dict]
VALID_CREATOR = UnionValidator[_VALIDATOR_CLASS, LITERALS, LITERAL_TYPES]


class LiteralValidator(BaseValidator):
    """
    Checks if data is in given objects
    Only works for literals!
    Literal classes are:
        str,
        int,
        float,
        bool
    and an constant:
        None
    """
    checking_type = LITERALS

    def parse_settings(self):
        assert len(self.settings) >= 1, "Give at least one arguments."

        for el in self.settings:
            assert isinstance(el, LITERALS), "Arguments shall be LITERALS"

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        return data in self.settings


class FormattedList(BaseValidator):
    checking_type = list

    def parse_settings(self):
        assert len(self.settings) >= 1, "Give at least one argument."

        for el in self.settings:
            assert isinstance(el, VALID_CREATOR), "Arguments shall be 'BaseValidator' subclass instances or LITERALS"

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        if len(self.settings) != len(data):
            return False

        for ind in range(len(data)):
            if not isinstance(data[ind], self.settings[ind]):
                return False

        return True


_DICT_KEYS = ArrayValidator[str]
_OPTIONAL_KEYS = ArrayValidator[str]


class FormattedDict(BaseValidator):
    checking_type = dict

    def parse_settings(self):
        assert len(self.settings) >= 2, "Give at least two arguments."

        if isinstance(self.settings[-1], _OPTIONAL_KEYS):
            optionals = self.settings[-1]
            settings = self.settings[:-1]
        else:
            optionals = ()
            settings = self.settings

        for el in settings:
            assert isinstance(el, tuple) and len(el) == 2 and isinstance(el[0], str) \
                and isinstance(el[1], VALID_CREATOR), \
                "Arguments have to be tuple of two elements, fist element is a string and second is " \
                "a valid type checker"

        self.info["dict"] = dict(settings)
        self.info["keys"] = set(self.info["dict"].keys())
        self.info["max_size"] = len(self.info["keys"])

        self.info["optionals"] = set(optionals)

        excepted = set()
        for e in self.info["keys"]:
            if e not in self.info["optionals"]:
                excepted.add(e)

        self.info["excepted"] = excepted

        self.info["min_size"] = self.info["max_size"] - len(self.info["optionals"])

    def validate(self, data: _TYPING_WITHOUT_VALIDATOR) -> bool:
        if not (isinstance(list(data.keys()), _DICT_KEYS)):
            # all keys shall be strings
            return False

        for key in data:
            if not isinstance(data[key], CHECKING_OBJECTS):
                # unexpected value type
                return False

            if key not in self.info["keys"]:
                # unexpected key
                return False

        for key in self.info["excepted"]:
            if key not in data:
                # missing key
                return False

            if not isinstance(data[key], self.info["dict"][key]):
                # failed type checking
                return False

        for key in self.info["optionals"]:
            if key not in data:
                # not specified
                continue

            if not isinstance(data[key], self.info["dict"][key]):
                # failed type checking
                return False

        return True
