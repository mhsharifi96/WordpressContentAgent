from functools import cache
import os
from client.request_data import BaseRequest
from domain.wordpress import WordPressPost, Category, Tag, Token

from dotenv import load_dotenv
load_dotenv()


class WordPressClient():
    def __init__(self, request_data: BaseRequest, base_url: str, username: str, password: str):
        self.request_data = request_data
        self.base_url = base_url
        self.username = username
        self.password = password

    async def get_posts(self, params: dict | None = None) -> dict:
        url = self.base_url + "/wp-json/wp/v2/posts"
        return await self.request_data.aget(url, params=params)

    async def get_post(self, post_id: int) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/posts/{post_id}"
        return await self.request_data.aget(url)
    
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
    
    async def get_categories(self) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/categories"
        return await self.request_data.aget(url)
    
    async def get_tags(self) -> dict:
        url = self.base_url + f"/wp-json/wp/v2/tags"
        return await self.request_data.aget(url)
    

    async def login_jwt(self) -> Token:
        url = self.base_url + f"/wp-json/jwt-auth/v1/token"
        headers = {"Content-Type": "application/json"}
        response = await self.request_data.apost(url, 
            data={"username": self.username, "password": self.password},
            headers=headers)
        return Token(**response)
    
    async def get_jwt_token(self):
        url = self.base_url + f"/wp-json/jwt-auth/v1/token"
        
        # JWT auth typically requires username and password in the body
        data = {
            "username": self.username,
            "password": self.password
        }
        
        # You might also need this header
        headers = {
            "Content-Type": "application/json"
        }
        
        response = await self.request_data.apost(url, data=data, headers=headers)
        print(response)
        return response


    
    async def validate_token(self, token: str) -> dict:
        url = self.base_url + f"/wp-json/jwt-auth/v1/token/validate"
        return await self.request_data.aget(url, headers={"Authorization": f"Bearer {token}"})


@cache 
def get_wp_client() -> WordPressClient:
    request_data = BaseRequest()
    username = os.getenv("WP_USERNAME")
    password = os.getenv("WP_PASSWORD")
    base_url = os.getenv("WP_BASE_URL")
    return WordPressClient(request_data, base_url, username, password)