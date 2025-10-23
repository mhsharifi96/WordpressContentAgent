from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    parent: int
    count: int

class Tag(BaseModel):
    id: int
    name: str
    slug: str

class WordPressPost(BaseModel):
    id: int
    title: str
    content: str
    date: str
    author: str
    category: Category | None = None
    tag: list[Tag] | None = None


class Token(BaseModel):
    token: str


