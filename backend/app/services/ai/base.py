from abc import ABC, abstractmethod
from typing import AsyncIterator

from pydantic import BaseModel


class RecognizedFoodItem(BaseModel):
    name: str
    confidence: float
    estimated_serving: str
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float


class FoodRecognitionResult(BaseModel):
    foods: list[RecognizedFoodItem]
    total_calories: float
    description: str = ""


class ExerciseRecognitionResult(BaseModel):
    exercise_type: str
    exercise_name: str
    estimated_duration_min: int | None = None
    calories_burned: float
    intensity: str | None = None
    confidence: float
    description: str = ""


class HealthPlanResult(BaseModel):
    summary: str
    daily_calorie_target: int
    daily_protein_g: float
    daily_fat_g: float
    daily_carbs_g: float
    daily_exercise_minutes: int
    calorie_deficit: int
    weekly_plans: list[dict]


class AIProvider(ABC):
    """AI 服务提供者抽象基类"""

    @abstractmethod
    async def analyze_food_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> FoodRecognitionResult:
        """识别食物图片，返回营养分析"""
        ...

    @abstractmethod
    async def analyze_exercise_image(
        self, image_base64: str, user_prompt: str = ""
    ) -> ExerciseRecognitionResult:
        """识别运动图片/截图，返回运动分析"""
        ...

    @abstractmethod
    async def chat(
        self, messages: list[dict], system_prompt: str = ""
    ) -> str:
        """对话接口，返回完整回复"""
        ...

    @abstractmethod
    async def chat_stream(
        self, messages: list[dict], system_prompt: str = ""
    ) -> AsyncIterator[str]:
        """流式对话接口，逐步返回回复内容"""
        ...

    @abstractmethod
    async def generate_health_plan(
        self, user_profile: dict, health_data: dict
    ) -> HealthPlanResult:
        """生成个性化健康计划"""
        ...
