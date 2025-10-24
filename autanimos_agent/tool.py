import logging
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from domain.wordpress import CreateWordPressPostData, Tag
from client.wp_client import WordPressClient, get_wp_client
from domain.wordpress import (
    Category,
    CategoryData,
    TagData,
    WordPressPostData,
    SimplePostData,
)
import settings

model = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)

client: WordPressClient = get_wp_client()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
async def get_posts() -> list[SimplePostData]:
    """Get all posts from the WordPress database.
    Returns:
        A list of posts.
    """
    logger.info("Getting all posts from the WordPress Api.")
    return await client.get_posts()


@tool
async def get_post(post_id: int) -> WordPressPostData:
    """Get a post from the WordPress api with the given post id.
    Args:
        post_id(int): The ID of the post to get.
    Returns:
        A WordPressPostData object.
    """
    logger.info(f"Getting post {post_id} from the WordPress database.")
    return await client.get_post(post_id)


@tool
async def get_tags() -> list[TagData]:
    """Get all tags from the WordPress api.
    Returns:
        A list of TagData objects.
    """
    logger.info("Getting all tags from the WordPress database.")
    return await client.get_tags()


@tool
async def get_tag(tag_id: int) -> TagData:
    """Get a tag from the WordPress api with the given tag id.
    Args:
        tag_id(int): The ID of the tag to get.
    Returns:
        A TagData object.
    """
    logger.info(f"Getting tag {tag_id} from the WordPress database.")
    return await client.get_tag(tag_id)


@tool
async def get_categories() -> list[CategoryData]:
    """Get all categories from the WordPress api.
    Returns:
        A list of CategoryData objects.
    """
    logger.info("Getting all categories from the WordPress database.")
    return await client.get_categories()


@tool
async def get_category(category_id: int) -> CategoryData:
    """Get a category from the WordPress api with the given category id.
    Args:
        category_id(int): The ID of the category to get.
    Returns:
        A CategoryData object.
    """
    logger.info(f"Getting category {category_id} from the WordPress database.")
    return await client.get_category(category_id)


@tool
async def create_tag(tag: Tag) -> TagData:
    """Create a tag in the WordPress api.
    Args:
        tag(Tag): The tag to create.
    Returns:
        A TagData object.
    """
    logger.info(f"Creating tag {tag.name} in the WordPress database.")
    return await client.create_tag(tag)


@tool
async def create_category(category: Category) -> CategoryData:
    """Create a category in the WordPress api.
    Args:
        category(Category): The category to create.
    Returns:
        A CategoryData object.
    """
    logger.info(f"Creating category {category.name} in the WordPress database.")
    return await client.create_category(category)


@tool
async def create_post(post: CreateWordPressPostData) -> bool:
    """Create a post in the WordPress api.
    Args:
        post(CreateWordPressPostData): The post to create.
    Returns:
        A boolean value indicating if the post was created successfully.
    """
    logger.info(f"Creating post {post.title} in the WordPress database.")
    result = await client.create_post(post)
    if result.id:
        return True
    else:
        return False


@tool
async def generate_content(content: str) -> str:
    """Generate a SEO content for a post.
    Args:
        content(str): The content to generate.
    Returns:
        A string.
    """
    logger.info(f"Generating content for {content}.")
    return await model.ainvoke(content)