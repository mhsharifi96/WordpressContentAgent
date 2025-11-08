from client.wp_client import get_wp_client
import asyncio

from pprint import pprint
from autanimos_agent.agent import  run_agent


wp_client = get_wp_client()




async def main():


    user_prompt = """عنوان پست :‌
تمرین Speaking با چت‌بات هوش مصنوعی LangAgent
کلمه کلیدی اصلی : 
آموزش مکالمه زبان با هوش مصنوعی
توضیح کوتاه :
راهنمای استفاده از چت‌بات برای تمرین مکالمه
با توجه به نکات seo بنویس 
حداقل ۷۰۰ کلمه
    """
    print("---------------Start Agent-----------------")
    result = await run_agent(user_prompt)

    pprint(result)
    print("---------------End Agent-----------------")


if __name__ == "__main__":
    asyncio.run(main())
