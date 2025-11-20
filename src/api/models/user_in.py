from typing import Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field


fake = Faker("en_US")


class UserRequest(BaseModel):
    username: Optional[str] = Field(..., description="Имя пользователя")
    email: Optional[str] = Field(..., description="Email пользователя")
    password: Optional[str] = Field(..., description="Пароль пользователя")

    @classmethod
    def random(
        cls
    ) -> "UserRequest":
        return cls(username=fake.user_name(), email=fake.email(), password=fake.password())
    
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        from_attributes=True
    )