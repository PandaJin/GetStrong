import json
import logging
from typing import AsyncIterator

import httpx

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


class KimiProvider(AIProvider):
    """Kimi (Moonshot) AI 服务实现"""

    def __init__(self):
        self.api_key = settings.KIMI_API_KEY
        self.base_url = settings.KIMI_BASE_URL
        self.model = settings.KIMI_MODEL

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _call_api(self, messages: list[dict], temperature: float = 0.3) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def analyze_food_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> FoodRecognitionResult:
        prompt = FOOD_RECOGNITION_PROMPT
        if user_prompt:
            prompt += f"\n\n用户补充说明：{user_prompt}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ]

        content = await self._call_api(messages, temperature=0.1)
        result = json.loads(content)
        return FoodRecognitionResult(**result)

    async def analyze_exercise_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> ExerciseRecognitionResult:
        prompt = EXERCISE_RECOGNITION_PROMPT
        if user_prompt:
            prompt += f"\n\n用户补充说明：{user_prompt}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ]

        content = await self._call_api(messages, temperature=0.1)
        result = json.loads(content)
        return ExerciseRecognitionResult(**result)

    async def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)
        return await self._call_api(all_messages, temperature=0.7)

    async def chat_stream(
        self, messages: list[dict], system_prompt: str = ""
    ) -> AsyncIterator[str]:
        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json={
                    "model": self.model,
                    "messages": all_messages,
                    "stream": True,
                    "temperature": 0.7,
                },
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue

    async def generate_health_plan(
        self, user_profile: dict, health_data: dict
    ) -> HealthPlanResult:
        prompt = HEALTH_PLAN_PROMPT.format(
            user_profile=json.dumps(user_profile, ensure_ascii=False, indent=2),
            health_data=json.dumps(health_data, ensure_ascii=False, indent=2),
        )
        messages = [{"role": "user", "content": prompt}]
        content = await self._call_api(messages, temperature=0.3)
        result = json.loads(content)
        return HealthPlanResult(**result)
