from functools import cache
import os
from client.request_data import BaseRequest
from domain.wordpress import (
    CategoryData,
    CreateWordPressPostData,
    GeneratePostData,
    TagData,
    WordPressPostData,
    Category,
    Tag,
    Token,
    SimplePostData,
)

from dotenv import load_dotenv

load_dotenv()


class WordPressClient:
    def __init__(
        self, request_data: BaseRequest, base_url: str, username: str, password: str
    ):
        self.request_data = request_data
        self.base_url = base_url
        self.username = username
        self.password = password

    async def get_posts(self) -> list[SimplePostData]:
        """Get all posts.
        Args:
            params(dict): The parameters to pass to the API.
        Returns:
            A list of WordPressPostData objects.
        """
        url = self.base_url + "/wp-json/wp/v2/posts"
        result = [
            await self._create_post_object(post, simple=True)
            for post in await self.request_data.aget(url)
        ]
        return result

    async def get_post(self, post_id: int) -> WordPressPostData:
        """Get a post by its ID.
        Args:
            post_id(int): The ID of the post to get.
        Returns:
            A WordPressPostData object.
        """
        url = self.base_url + f"/wp-json/wp/v2/posts/{post_id}"
        reponse = await self.request_data.aget(url)
        post_obj = await self._create_post_object(reponse)
        return post_obj

    async def get_post_by_slug(self, post_slug: str) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/posts?slug={post_slug}"
        return await self.request_data.aget(url)

    async def get_post_by_title(self, post_title: str) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/posts?search={post_title}"
        return await self.request_data.aget(url)

    async def get_post_by_category(self, category_id: int) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/posts?category={category_id}"
        return await self.request_data.aget(url)

    async def get_post_by_tag(self, tag_id: int) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/posts?tag={tag_id}"
        return await self.request_data.aget(url)

    async def get_categories(self) -> list[CategoryData]:
        """Get all categories.
        Returns:
            A list of Category objects.
        """
        url = self.base_url + "/wp-json/wp/v2/categories"
        return [
            CategoryData(**category) for category in await self.request_data.aget(url)
        ]

    async def get_category(self, category_id: int) -> CategoryData:
        """Get a category by its ID.
        Args:
            category_id(int): The ID of the category to get.
        Returns:
            A Category object.
        """
        url = self.base_url + f"/wp-json/wp/v2/categories/{category_id}"
        category = await self.request_data.aget(url)
        return CategoryData(**category)

    async def get_tags(self) -> list[TagData]:
        """Get all tags.
        Returns:
            A list of Tag objects.
        """
        url = self.base_url + "/wp-json/wp/v2/tags"
        return [TagData(**tag) for tag in await self.request_data.aget(url)]

    async def get_tag(self, tag_id: int) -> TagData:
        """Get a tag by its ID.
        Args:
            tag_id(int): The ID of the tag to get.
        Returns:
            A Tag object.
        """
        url = self.base_url + f"/wp-json/wp/v2/tags/{tag_id}"
        tag = await self.request_data.aget(url)
        return TagData(**tag)

    async def create_tag(self, tag: Tag) -> TagData:
        """Create a tag.
        Args:
            tag(Tag): The tag to create.
        Returns:
            A TagData object.
        """
        url = self.base_url + "/wp-json/wp/v2/tags"
        token = await self.login_jwt()
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token.token}",
        }
        return TagData(
            **await self.request_data.apost(url, data=tag.model_dump(), headers=header)
        )

    async def create_category(self, category: Category) -> CategoryData:
        """Create a category.
        Args:
            category(Category): The category to create.
        Returns:
            A Category object.
        """
        url = self.base_url + "/wp-json/wp/v2/categories"
        token = await self.login_jwt()
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token.token}",
        }
        return CategoryData(
            **await self.request_data.apost(
                url, data=category.model_dump(), headers=header
            )
        )

    async def create_post(self, post: CreateWordPressPostData) -> SimplePostData:
        """Create a post.
        Args:
            post(CreateWordPressPostData): The post to create.
        Returns:
            A WordPressPostData object.
        """
        url = self.base_url + "/wp-json/wp/v2/posts"
        token = await self.login_jwt()
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token.token}",
        }
        response = await self.request_data.apost(
            url, data=post.model_dump(), headers=header
        )
        return await self._create_post_object(response, simple=True)

    async def create_post_with_categories_and_tags(
        self, post: GeneratePostData
    ) -> bool:
        """Create a post with categories and tags.
        Args:
            post(GeneratePostData): The post data object containing title, content, tags, and categories.
        Returns:
            A WordPressPostData object.
        """
        categories = []
        tags = []
        if post.categories:
            categories = [
                (await self.create_category(category)).id
                for category in post.categories
            ]
        if post.tags:
            tags = [(await self.create_tag(tag)).id for tag in post.tags]

        wp_post_dict = {
            "title": post.title,
            "content": post.content,
            "slug": post.slug,
            "date": post.date,
            "categories": categories,
            "tags": tags,
        }
        response = await self.create_post(CreateWordPressPostData(**wp_post_dict))
        return bool(response.id)

    async def login_jwt(self) -> Token:
        url = self.base_url + "/wp-json/jwt-auth/v1/token"
        headers = {"Content-Type": "application/json"}
        response = await self.request_data.apost(
            url,
            data={"username": self.username, "password": self.password},
            headers=headers,
        )
        return Token(**response)

    async def _create_post_object(
        self, data: dict, simple: bool = False
    ) -> WordPressPostData | SimplePostData:
        category_ids = data.get("categories", [])
        tag_ids = data.get("tags", [])

        # Prepare all data before creating the object
        post_data = {
            "id": data.get("id"),
            "title": data.get("title", {}).get("rendered"),
            "content": data.get("content", {}).get("rendered"),
            "slug": data.get("slug"),
            "date": data.get("modified"),
        }

        if simple:
            obj = SimplePostData(**post_data, categories=category_ids, tags=tag_ids)
            obj.content = None
            return obj

        wordpress_post = WordPressPostData(**post_data)
        wordpress_post.categories = (
            [await self.get_category(cat_id) for cat_id in category_ids]
            if category_ids
            else []
        )
        wordpress_post.tags = (
            [await self.get_tag(tag_id) for tag_id in tag_ids] if tag_ids else []
        )
        return wordpress_post

    async def validate_token(self, token: str) -> dict:
        url = self.base_url + "/wp-json/jwt-auth/v1/token/validate"
        return await self.request_data.aget(
            url, headers={"Authorization": f"Bearer {token}"}
        )


@cache
def get_wp_client() -> WordPressClient:
    request_data = BaseRequest()
    username = os.getenv("WP_USERNAME")
    password = os.getenv("WP_PASSWORD")
    base_url = os.getenv("WP_BASE_URL")
    return WordPressClient(request_data, base_url, username, password)
