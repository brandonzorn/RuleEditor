import abc
from datetime import datetime
from enum import Enum

from dateutil.parser import parse


class AbstractAttributeType(abc.ABC):
    NAME: str
    VALID_VALUES = []

    @classmethod
    def get_valid_values(cls) -> list[str]:
        return cls.VALID_VALUES

    @staticmethod
    def validate(value: str) -> bool:
        return True


class NumericAttribute(AbstractAttributeType):
    NAME = "Числовое"

    @staticmethod
    def validate(value: str) -> bool:
        return value.isdigit()


class SymbolicAttribute(AbstractAttributeType):
    NAME = "Символьное"


class BooleanAttribute(AbstractAttributeType):
    NAME = "Логическое"
    VALID_VALUES = ["ИСТИНА", "ЛОЖЬ"]

    @classmethod
    def get_valid_values(cls) -> list[str]:
        return cls.VALID_VALUES

    @classmethod
    def validate(cls, value: str) -> bool:
        return value in cls.VALID_VALUES


class DateAttribute(AbstractAttributeType):
    NAME = "Дата"

    @classmethod
    def validate(cls, value: str) -> bool:
        try:
            date = parse(value, default=datetime(9999, 12, 31))
        except ValueError:
            return False
        return not (date.year == 9999)


class LinguisticVarAttribute(AbstractAttributeType):
    NAME = "Лингвистическая переменная"


class AttributeTypeEnum(Enum):
    NUMERIC = NumericAttribute
    SYMBOLIC = SymbolicAttribute
    BOOLEAN = BooleanAttribute
    DATE = DateAttribute
    LINGUISTIC_VAR = LinguisticVarAttribute

    @classmethod
    def from_id(cls, attr_id: int):
        members = list(cls)
        if 0 <= attr_id < len(members):
            return members[attr_id]
        raise ValueError(f"No AttributeTypeEnum with id={attr_id}")

    def to_id(self):
        members = list(AttributeTypeEnum)
        return members.index(self)


class Attribute:
    def __init__(
            self,
            attr_id: int,
            name: str,
            attr_type: AttributeTypeEnum,
            non_default_values: list[str] | None = None,
    ):
        self.attr_id = attr_id
        self.name = name
        self._attr_type = attr_type
        self.non_default_values = non_default_values
        if non_default_values is None:
            self.non_default_values = []

    @property
    def attr_type(self):
        return self._attr_type.value

    def get_valid_values(self):
        if self.non_default_values:
            return self.non_default_values
        return self.attr_type.get_valid_values()

    def validate(self, value):
        return self.attr_type.validate(value)

    def get_name(self):
        return f"{self.name} - {self.attr_type.NAME}"

    def to_dict(self):
        return {
            "attr_id": self.attr_id,
            "name": self.name,
            "attr_type_id": self._attr_type.to_id(),
            "ndv": self.non_default_values,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            attr_id=data["attr_id"],
            name=data["name"],
            attr_type=AttributeTypeEnum.from_id(data["attr_type_id"]),
            non_default_values=data.get("ndv", None),
        )
