from typing import Optional

from faker import Faker
from pydantic import Field

from .base import BaseAPIModel as Base

fake = Faker("en_US")


class Capabilities(Base):
    read: bool
    level_0: bool
    subscriber: bool


class ExtraCapabilities(Base):
    subscriber: bool


class UserCreationRequest(Base):
    username: Optional[str] = Field(..., description="Имя пользователя")
    email: Optional[str] = Field(..., description="Email пользователя")
    password: Optional[str] = Field(..., description="Пароль пользователя")

    @classmethod
    def random(cls) -> "UserCreationRequest":
        return cls(
            username=fake.user_name(), email=fake.email(), password=fake.password()
        )


class UserCreationResponse(Base):
    id: int = Field(..., description="ID пользователя")
    username: str = Field(..., description="Имя пользователя")
    name: str = Field(..., description="Имя")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    email: str = Field(..., description="Email пользователя")
    url: str = Field(..., description="URL пользователя")
    description: str = Field(..., description="Описание пользователя")
    link: str = Field(..., description="Ссылка на пользователя")
    locale: str = Field(..., description="Локаль пользователя")
    nickname: str = Field(..., description="Псевдоним пользователя")
    slug: str = Field(..., description="Слаг пользователя")
    roles: list[str] = Field(..., description="Роли пользователя")
    registered_date: Optional[str] = Field(
        None, description="Дата регистрации пользователя"
    )
    capabilities: Capabilities = Field(..., description="Возможности пользователя")
    extra_capabilities: ExtraCapabilities = Field(
        ..., description="Дополнительные возможности пользователя"
    )


class UserPublicResponse(Base):
    id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Имя пользователя")
    url: str = Field(..., description="URL пользователя")
    description: str = Field(..., description="Описание пользователя")
    link: str = Field(..., description="Ссылка на пользователя")
    slug: str = Field(..., description="Слаг пользователя")
