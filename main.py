from client.wp_client import get_wp_client
import asyncio

from pprint import pprint
from autanimos_agent.agent import  run_agent


wp_client = get_wp_client()




async def main():
    # token = await wp_client.login_jwt()
    # print(token.token)
    # posts = await wp_client.get_posts()
    # pprint(posts[0])
    # categories = await wp_client.get_categories()
    # pprint(categories[0])
    # print("--------------------------------")
    # tags = await wp_client.get_tags()
    # pprint(tags[0])
    # category = await wp_client.get_category(67)
    # pprint(category)
    # print("--------------------------------")
    # tag = await wp_client.get_tag(162)
    # pprint(tag)
    # posts = await wp_client.get_posts()
    # pprint(posts)
    # post = await wp_client.get_post(360)
    # pprint(post)
    # print("--------------------------------")
    # tag = Tag(name="Test Tag1", slug="test-tag1")
    # created_tag = await wp_client.create_tag(tag)
    # pprint(created_tag)
    # post = SimplePostData(title="Test Post1", content="This is a test post", slug="test-post1")
    # created_post = await wp_client.create_post(post)
    # pprint(created_post)

    user_prompt = """
    عنوان: آموزش مکالمه زبان با هوش مصنوعی در اپ LangAgent
    کلمه کلیدی: آموزش مکالمه زبان با هوش مصنوعی
    هدف: آگاهی
    توضیح: معرفی مزایای استفاده از هوش مصنوعی در یادگیری مکالمه
     100 کلمه
    """
    print("---------------Start Agent-----------------")
    result = await run_agent(user_prompt)

    pprint(result)
    print("---------------End Agent-----------------")


if __name__ == "__main__":
    asyncio.run(main())
