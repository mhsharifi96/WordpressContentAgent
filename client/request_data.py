import asyncio
import aiohttp


class BaseRequest():

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    async def aget(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict:
        """Send an asynchronous GET request."""
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                response.raise_for_status()
                return await response.json()

    async def apost(self, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
        """Send an asynchronous POST request."""
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(url, json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                response.raise_for_status()
                return await response.json()


async def get_jwt_token(username: str, password: str):
    request = BaseRequest()
    
    url = "https://blog.langagent.ir/wp-json/jwt-auth/v1/token"
    
    # JWT auth typically requires username and password in the body
    data = {
        "username": username,
        "password": password
    }
    
    # You might also need this header
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = await request.apost(url, data=data, headers=headers)
        print(response)
        return response
    except aiohttp.ClientResponseError as e:
        print(f"Error: {e.status} - {e.message}")
        raise



# if __name__ == "__main__":
#     asyncio.run(get_jwt_token("admin", "F@temeh110"))