from typing import Any

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

fake = Faker("en_US")


class PostRequest(BaseModel):
    title: str = Field(..., description="Заголовок статьи")
    content: str = Field(..., description="Содержимое статьи")
    status: str = Field(..., description="Статус статьи")

    @classmethod
    def random(
        cls, empty: bool = False, status: str | Any = "publish"
    ) -> "PostRequest":
        if empty:
            return cls(title="", content="", status=status)
        return cls(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            status=status,
        )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
