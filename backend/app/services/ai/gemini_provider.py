import base64
import json
import logging
from typing import AsyncIterator

import google.generativeai as genai

from app.core.config import settings
from app.services.ai.base import (
    AIProvider,
    ExerciseRecognitionResult,
    FoodRecognitionResult,
    HealthPlanResult,
)
from app.services.ai.prompts import (
    EXERCISE_RECOGNITION_PROMPT,
    FOOD_RECOGNITION_PROMPT,
    HEALTH_PLAN_PROMPT,
)

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    """Google Gemini AI 服务实现"""

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def _make_image_part(self, image_base64: str) -> dict:
        return {
            "mime_type": "image/jpeg",
            "data": base64.b64decode(image_base64),
        }

    async def analyze_food_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> FoodRecognitionResult:
        prompt = FOOD_RECOGNITION_PROMPT
        if user_prompt:
            prompt += f"\n\n用户补充说明：{user_prompt}"

        image_part = self._make_image_part(image_base64)
        response = await self.model.generate_content_async(
            [prompt, image_part],
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )
        result = json.loads(response.text)
        return FoodRecognitionResult(**result)

    async def analyze_exercise_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> ExerciseRecognitionResult:
        prompt = EXERCISE_RECOGNITION_PROMPT
        if user_prompt:
            prompt += f"\n\n用户补充说明：{user_prompt}"

        image_part = self._make_image_part(image_base64)
        response = await self.model.generate_content_async(
            [prompt, image_part],
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )
        result = json.loads(response.text)
        return ExerciseRecognitionResult(**result)

    async def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        chat_model = genai.GenerativeModel(
            settings.GEMINI_MODEL,
            system_instruction=system_prompt if system_prompt else None,
        )

        # Convert messages to Gemini format
        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = chat_model.start_chat(history=history)
        last_msg = messages[-1]["content"] if messages else ""
        response = await chat.send_message_async(last_msg)
        return response.text

    async def chat_stream(
        self, messages: list[dict], system_prompt: str = ""
    ) -> AsyncIterator[str]:
        chat_model = genai.GenerativeModel(
            settings.GEMINI_MODEL,
            system_instruction=system_prompt if system_prompt else None,
        )

        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = chat_model.start_chat(history=history)
        last_msg = messages[-1]["content"] if messages else ""

        response = await chat.send_message_async(last_msg, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def generate_health_plan(
        self, user_profile: dict, health_data: dict
    ) -> HealthPlanResult:
        prompt = HEALTH_PLAN_PROMPT.format(
            user_profile=json.dumps(user_profile, ensure_ascii=False, indent=2),
            health_data=json.dumps(health_data, ensure_ascii=False, indent=2),
        )
        response = await self.model.generate_content_async(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json",
            ),
        )
        result = json.loads(response.text)
        return HealthPlanResult(**result)
