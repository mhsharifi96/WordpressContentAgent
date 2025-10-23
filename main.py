from client.wp_client import get_wp_client
import asyncio
from pprint import pprint
wp_client = get_wp_client()

async def main():
    # token = await wp_client.login_jwt()
    # print(token.token)
    # posts = await wp_client.get_posts()
    # pprint(posts[0])
    categories = await wp_client.get_categories()
    pprint(categories[0])
    print("--------------------------------")
    tags = await wp_client.get_tags()
    pprint(tags[0])
   
if __name__ == "__main__":
    asyncio.run(main())