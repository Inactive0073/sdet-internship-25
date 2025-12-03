from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from faker import Faker
from pydantic import Field

from .base import BaseAPIModel as Base

fake = Faker("en_US")


class Title(Base):
    raw: str | None = None
    rendered: str


class Content(Base):
    raw: str | None = None
    rendered: str
    protected: bool

    @property
    def text(self) -> str:
        """
        Возвращает чистый текст без HTML-тегов.
        Если raw есть — используем её.
        Если raw нет — очищаем rendered от HTML.
        """
        source = self.raw or self.rendered
        soup = BeautifulSoup(source, "html.parser")
        return soup.get_text().strip()


class PostCreationRequest(Base):
    title: str = Field(..., description="Заголовок статьи")
    content: str = Field(..., description="Содержимое статьи")
    status: str = Field(..., description="Статус статьи")

    @classmethod
    def random(
        cls, empty: bool = False, status: str | Any = "publish"
    ) -> "PostCreationRequest":
        if empty:
            return cls(title="", content="", status=status)
        return cls(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            status=status,
        )


class PostCreationResponse(Base):
    id: int
    slug: str
    status: str
    date: datetime
    modified: datetime
    title: Title
    content: Content
