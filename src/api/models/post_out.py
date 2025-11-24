from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Title(BaseModel):
    raw: str | None = None
    rendered: str

    model_config = ConfigDict(extra="ignore")


class Content(BaseModel):
    raw: str | None = None
    rendered: str
    protected: bool

    model_config = ConfigDict(extra="ignore")


class PostResponse(BaseModel):
    id: int
    slug: str
    status: str
    date: datetime
    modified: datetime
    title: Title
    content: Content

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        from_attributes=True,
    )
