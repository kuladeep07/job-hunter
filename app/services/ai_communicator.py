from typing import Type

from google import genai
from pydantic import BaseModel

from app.core.configs.settings import settings

genai_client = genai.Client(api_key=settings.ai_api_key)

async def aichat_structured_response(prompt: str, schema: Type[BaseModel]):
    try:
        interaction = genai_client.interactions.create(model=settings.model_name, input=prompt, response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": schema.model_json_schema()
        })
        return schema.model_validate_json(interaction.output_text)
    except Exception as e:
        return None