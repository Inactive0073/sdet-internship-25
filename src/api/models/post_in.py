from typing import Any, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field, field_validator

fake = Faker("en_US")


class PostRequest(BaseModel):
    title: str = Field(..., description="Заголовок статьи")
    content: str = Field(..., description="Содержимое статьи")
    status: str = Field(..., description="Статус статьи")


    @field_validator('status', mode='before')
    @classmethod
    def ensure_status(cls, v: Any):
        if v not in ["draft", "publish", "future", "pending", "private"]:
            raise ValueError(f'"{v}" not found in allowed status values')
        return v

    @classmethod
    def random(cls, empty: bool = False, status: str = "publish") -> "PostRequest":
        if empty:
            return cls(title="", content="", status=status)
        return cls(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            status=status
        )
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )