from datetime import datetime
from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    slug: str
    description: str | None = None
    parent: int | None = None
    count: int | None = None


class CategoryData(Category):
    id: int


class Tag(BaseModel):
    name: str = Field(description="The name of the tag")
    slug: str = Field(description="The slug of the tag")


class TagData(Tag):
    id: int


class BaseWordPressPost(BaseModel):
    title: str
    content: str
    slug: str = Field(description="The slug of the post should be english and unique")
    date: str = datetime.now().isoformat()
    categories: list[Category] | None = None
    tags: list[Tag] | None = None


class GeneratePostData(BaseModel):
    title: str
    content: str
    slug: str
    date: str = datetime.now().isoformat()
    categories: list[Category] = Field(
        description="The categories should be related to the content of the post"
    )
    tags: list[Tag] = Field(
        description="The tags should be related to the content of the post"
    )


class WordPressPostData(BaseWordPressPost):
    id: int


class SimplePostData(BaseWordPressPost):
    id: int | None = None
    content: str | None = None
    categories: list[int] | None = None
    tags: list[int] | None = None


class CreateWordPressPostData(BaseWordPressPost):
    id: int | None = None
    categories: list[int] | None = None
    tags: list[int] | None = None
    status: str = "publish"


class Token(BaseModel):
    token: str


class PostContext(BaseModel):
    user_prompt: str
