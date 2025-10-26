from typing import Any
from langchain.agents import create_agent
from autanimos_agent.model import get_model
from autanimos_agent.prompts import AGENT_SYSTEM_PROMPT, AGENT_SYSTEM_PROMPT_1
import autanimos_agent.tool as tool_wp
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain.messages import HumanMessage
from domain.wordpress import PostContext

langfuse = get_client()


tools = [
    tool_wp.generate_content,
    # tool_wp.create_tag,
    # tool_wp.create_category,
    tool_wp.create_post,
    # tool_wp.get_posts,
    # tool_wp.get_post,
    # tool_wp.get_tags,
    # tool_wp.get_tag,
    # tool_wp.get_categories,
    # tool_wp.get_category,
]


def get_agent() -> Any:
    model = get_model()
    # TODO: Add content and command for handle tool runtime.

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=AGENT_SYSTEM_PROMPT_1,
        context_schema=PostContext,
    )


async def run_agent(user_prompt: str) -> Any:
    langfuse_handler = CallbackHandler()
    agent = get_agent()
    messages = [HumanMessage(content=user_prompt)]

    return await agent.ainvoke(
        {"messages": messages},
        config={"callbacks": [langfuse_handler]},
        context=PostContext(user_prompt=user_prompt),
    )
