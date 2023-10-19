from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class ShowBlog(BaseModel):
    title: str
    content: Optional[str] = None
    created_at: date
    model_config = ConfigDict(from_atributes=True)


class UpdateBlog(CreateBlog):
    pass
