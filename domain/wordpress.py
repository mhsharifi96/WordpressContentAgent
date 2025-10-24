from datetime import datetime
from pydantic import BaseModel


class Category(BaseModel):
    name: str
    slug: str
    description: str
    parent: int
    count: int

class CategoryData(Category):
    id: int
    

class Tag(BaseModel):
    name: str
    slug: str

class TagData(Tag):
    id: int

class BaseWordPressPost(BaseModel):
    title: str
    content: str
    slug :str
    date: str = datetime.now().isoformat()
    categories: list[Category] | None = None
    tags: list[Tag] | None = None

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





class Token(BaseModel):
    token: str


