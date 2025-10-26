from functools import cache
import logging
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from autanimos_agent.model import get_model
from autanimos_agent.prompts import CREATE_CATEGORY_PROMPT, CREATE_TAG_PROMPT
from domain.wordpress import CreateWordPressPostData, GeneratePostData, Tag
from client.wp_client import WordPressClient, get_wp_client
from domain.wordpress import (
    Category,
    CategoryData,
    TagData,
    WordPressPostData,
    SimplePostData,
    PostContext,
)
from langgraph.types import Command

client: WordPressClient = get_wp_client()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
async def get_posts() -> list[SimplePostData]:
    """
    Retrieve all posts from the WordPress API.

    Returns:
        list[SimplePostData]: A list of post data objects retrieved from the WordPress API.
    """
    logger.info("Getting all posts from the WordPress API.")
    return await client.get_posts()


@tool
async def get_post(post_id: int) -> WordPressPostData:
    """
    Retrieve a specific post from the WordPress API by its ID.

    Args:
        post_id (int): The unique identifier of the post to retrieve.

    Returns:
        WordPressPostData: The post data object corresponding to the given ID.
    """
    logger.info(f"Getting post {post_id} from the WordPress API.")
    return await client.get_post(post_id)


@tool
async def get_tags() -> list[TagData]:
    """
    Retrieve all tags from the WordPress API.

    Returns:
        list[TagData]: A list of tag data objects retrieved from the WordPress API.
    """
    logger.info("Getting all tags from the WordPress API.")
    return await client.get_tags()


@tool
async def get_tag(tag_id: int) -> TagData:
    """
    Retrieve a specific tag from the WordPress API by its ID.

    Args:
        tag_id (int): The unique identifier of the tag to retrieve.

    Returns:
        TagData: The tag data object corresponding to the given ID.
    """
    logger.info(f"Getting tag {tag_id} from the WordPress API.")
    return await client.get_tag(tag_id)


@tool
async def get_categories() -> list[CategoryData]:
    """
    Retrieve all categories from the WordPress API.

    Returns:
        list[CategoryData]: A list of category data objects retrieved from the WordPress API.
    """
    logger.info("Getting all categories from the WordPress API.")
    return await client.get_categories()


@tool
async def get_category(category_id: int) -> CategoryData:
    """
    Retrieve a specific category from the WordPress API by its ID.

    Args:
        category_id (int): The unique identifier of the category to retrieve.

    Returns:
        CategoryData: The category data object corresponding to the given ID.
    """
    logger.info(f"Getting category {category_id} from the WordPress API.")
    return await client.get_category(category_id)


@tool
async def create_tag(input_prompt: str) -> list[TagData] | None:
    """
    Generate and create new tags in the WordPress API using an input prompt.

    The function uses an AI model to generate tag names based on the input prompt,
    then creates the generated tags in WordPress.

    Args:
        input_prompt (str): The textual prompt used to generate tags.

    Returns:
        list[TagData] | None:
            A list of created tag data objects if successful, otherwise None.
    """
    logger.info(
        f"Generating tags using input prompt '{input_prompt}' and creating them in WordPress."
    )
    model = get_model()
    model_with_structure = model.with_structured_output(list[Tag])
    generated_tags = await model_with_structure.ainvoke(
        CREATE_TAG_PROMPT.format(input_prompt=input_prompt)
    )
    create_tags: list[TagData] | None = None
    if generated_tags:
        create_tags = [await client.create_tag(tag) for tag in generated_tags]
        logger.info(f"Created tags {create_tags} in the WordPress API.")
    return create_tags


@tool
async def create_category(input_prompt: str) -> CategoryData | None:
    """
    Generate and create a new category in the WordPress API using an input prompt.

    The function uses an AI model to generate a category name based on the input prompt,
    then creates the generated category in WordPress.

    Args:
        input_prompt (str): The textual prompt used to generate the category.

    Returns:
        CategoryData | None:
            The created category data object if successful, otherwise None.
    """
    model = get_model()
    model_with_structure = model.with_structured_output(Category)
    generated_category = await model_with_structure.ainvoke(
        CREATE_CATEGORY_PROMPT.format(input_prompt=input_prompt)
    )
    if generated_category:
        category = await client.create_category(generated_category)
        return category
    else:
        return None





@tool(
    "generate_content",
    description="Generate SEO-optimized content with category and tags for a WordPress post using an AI model.",
)
async def generate_content(runtime: ToolRuntime[PostContext]) -> Command[GeneratePostData]:
    """
    Generate SEO-optimized content for a WordPress post using an AI model.

    Args:
        runtime (ToolRuntime): The runtime of the tool.
    Returns:
        str: The AI-generated SEO-optimized content.
    """
    model = get_model()
    # messages = runtime.state["messages"]
    # Access the latest user message
    # human_msg = [m for m in messages if m.__class__.__name__ == "HumanMessage"][-1]
    model = model.with_structured_output(GeneratePostData)
    user_prompt = runtime.context.user_prompt
    tool_call_id = runtime.tool_call_id

    logger.info(f"Generating SEO-optimized content for input: {user_prompt}.")

    response = await model.ainvoke(user_prompt)
    return Command(
        update={
            "generated_post": response,
            "messages":[ToolMessage(content="SEO content generated successfully.", tool_call_id=tool_call_id)],
        },
        
    )
@tool
async def create_post( post: GeneratePostData, runtime: ToolRuntime) -> bool:
    """
    Create a new post in the WordPress API.

    Args:
        post (GeneratePostData): The post data object containing title, content, tags, and categories.
        runtime (ToolRuntime): The runtime of the tool.

    Returns:
        bool: True if the post was created successfully, False otherwise.
    """
    result = await client.create_post_with_categories_and_tags(post)
    return result