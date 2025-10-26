# WP Content Agent

An intelligent WordPress content management agent powered by LangChain and OpenAI. This agent automatically generates SEO-optimized blog posts with categories and tags, and publishes them to your WordPress site via the REST API.

## Features

- 🤖 **AI-Powered Content Generation**: Generate high-quality, SEO-optimized blog posts using GPT-4
- 🏷️ **Smart Categorization**: Automatically create and assign relevant categories and tags
- 🔐 **JWT Authentication**: Secure authentication with WordPress using JWT tokens
- 🌐 **Async Operations**: Built with async/await for efficient API interactions
- 📊 **LangGraph Integration**: Structured agent workflow with tool calling capabilities
- 📝 **Persian/English Support**: Supports content generation in multiple languages
- 🔍 **Langfuse Monitoring**: Track and monitor AI agent executions

## Requirements

- Python 3.12+
- WordPress site with:
  - [JWT Authentication for WP REST API](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/) plugin
  - REST API enabled

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd wp_content_agent
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
# WordPress Configuration
WP_BASE_URL=https://your-wordpress-site.com
WP_USERNAME=your-username
WP_PASSWORD=your-password

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: custom endpoint

# Langfuse Configuration (Optional)
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Project Structure

```
wp_content_agent/
├── autanimos_agent/          # AI agent implementation
│   ├── agent.py              # Agent configuration and execution
│   ├── model.py              # OpenAI model initialization
│   ├── prompts.py            # System prompts for content generation
│   └── tool.py               # WordPress API tools
├── client/                    # WordPress API client
│   ├── request_data.py       # HTTP request handler with SSL support
│   └── wp_client.py          # WordPress REST API wrapper
├── domain/                    # Domain models
│   └── wordpress.py          # Pydantic models for WordPress entities
├── main.py                    # Application entry point
├── settings.py               # Application settings
└── requirements.txt          # Python dependencies
```

## Usage

### Basic Usage

Run the agent with a content generation prompt:

```python
from autanimos_agent.agent import run_agent
import asyncio

async def main():
    user_prompt = """
    Title: Improve IELTS Listening Skills with LangAgent
    Main Keyword: IELTS with AI
    Content Idea: Practice listening exercises for IELTS on the website
    Minimum 700 words
    """
    
    result = await run_agent(user_prompt)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```


### Direct WordPress Client Usage

```python
from client.wp_client import get_wp_client

wp_client = get_wp_client()

# Authenticate
token = await wp_client.login_jwt()

# Get posts
posts = await wp_client.get_posts()

# Create a post
post_data = GeneratePostData(
    title="My Blog Post",
    content="<p>Post content here</p>",
    slug="my-blog-post",
    categories=[Category(name="Tech", slug="tech")],
    tags=[Tag(name="AI", slug="ai")]
)
result = await wp_client.create_post_with_categories_and_tags(post_data)
```

## How It Works

1. **User Input**: Provide a prompt with title, keywords, and content requirements
2. **AI Processing**: The agent uses GPT-4 to generate:
   - SEO-optimized content
   - Relevant categories
   - Appropriate tags
   - URL-friendly slug
3. **WordPress Integration**: Automatically creates categories/tags if they don't exist
4. **Publishing**: Publishes the complete post to WordPress

## Configuration

### SSL Certificate Handling

The client automatically handles SSL verification issues. SSL verification is disabled by default for development environments. To modify:

```python
# In client/request_data.py
async with aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(ssl=False)  # Set to True for production
) as session:
    ...
```

### Model Configuration

Change the AI model in `autanimos_agent/model.py`:

```python
model = init_chat_model(
    model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo"
    model_provider="openai",
    api_key=settings.OPENAI_API_KEY,
)
```

## Logging

The application uses Python's built-in logging. Configure logging level:

```python
import logging
logging.basicConfig(level=logging.INFO)  # DEBUG, INFO, WARNING, ERROR
```

## Troubleshooting

### SSL Certificate Errors
If you encounter SSL certificate verification errors, the client is configured to handle them automatically.

### JWT Authentication Issues
Ensure the JWT Authentication plugin is properly configured in WordPress:
1. Install and activate the plugin
2. Configure `.htaccess` or nginx for Authorization headers
3. Set JWT secret in `wp-config.php`

### API Connection Issues
- Verify `WP_BASE_URL` is correct and accessible
- Check WordPress REST API is enabled
- Ensure firewall/security plugins allow REST API access

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.
