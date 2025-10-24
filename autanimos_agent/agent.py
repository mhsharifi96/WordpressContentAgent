from typing import Any
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from autanimos_agent.prompts import AGENT_SYSTEM_PROMPT
import autanimos_agent.tool as tool_wp
import settings
from langfuse import get_client
from langfuse.langchain import CallbackHandler

langfuse = get_client()

model = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


tools = [
    tool_wp.generate_content,
    tool_wp.get_posts,
    tool_wp.get_post,
    tool_wp.get_tags,
    tool_wp.get_tag,
    tool_wp.get_categories,
    tool_wp.get_category,
    tool_wp.create_tag,
    tool_wp.create_category,
    tool_wp.create_post,
]


def get_agent() -> Any:
    return create_agent(model=model, tools=tools, system_prompt=AGENT_SYSTEM_PROMPT)


async def run_agent(user_prompt: str) -> Any:
    langfuse_handler = CallbackHandler()
    agent = get_agent()
    return await agent.ainvoke(
        {"role": "user", "input": user_prompt}, config={"callbacks": [langfuse_handler]}
    )
