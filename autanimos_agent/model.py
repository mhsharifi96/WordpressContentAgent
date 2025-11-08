


from functools import cache
from langchain.chat_models import init_chat_model
import settings

@cache
def get_model():
    model = init_chat_model(
        model=settings.CHAT_MODEL,
        model_provider=settings.MODEL_PROVIDER,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    return model
