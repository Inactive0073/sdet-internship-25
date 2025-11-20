from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Capabilities(BaseModel):
    read: bool
    level_0: bool
    subscriber: bool

    model_config = ConfigDict(extra="ignore")

class ExtraCapabilities(BaseModel):
    subscriber: bool

    model_config = ConfigDict(extra="ignore")


class UserResponse(BaseModel):
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
    registered_date: Optional[str] = Field(None, description="Дата регистрации пользователя")
    capabilities: Capabilities = Field(..., description="Возможности пользователя")
    extra_capabilities: ExtraCapabilities = Field(..., description="Дополнительные возможности пользователя")

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        from_attributes=True,
    )