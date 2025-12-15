import json
from dataclasses import asdict, dataclass, fields
from typing import Type, TypeVar

T = TypeVar("T", bound="BaseDataClass")


@dataclass
class BaseDataClass:
    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        if not data:
            return cls()

        class_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in class_fields}
        return cls(**filtered_data)

    def to_dict(self) -> dict:
        """Сериализует объект в словарь."""
        return asdict(self)

    def to_json(self) -> str:
        """Сериализует объект в JSON строку."""
        return json.dumps(self.to_dict())
