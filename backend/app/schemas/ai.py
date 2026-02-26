from pydantic import BaseModel


class RecognizedFood(BaseModel):
    name: str
    confidence: float
    estimated_serving: str
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float


class FoodRecognitionResponse(BaseModel):
    recognition_id: str
    foods: list[RecognizedFood]
    total_calories: float
    ai_provider: str


class RecognizedExercise(BaseModel):
    exercise_type: str
    exercise_name: str
    estimated_duration_min: int | None = None
    calories_burned: float
    intensity: str | None = None
    confidence: float


class ExerciseRecognitionResponse(BaseModel):
    recognition_id: str
    exercise: RecognizedExercise
    ai_provider: str


class ImageRecognitionRequest(BaseModel):
    image_url: str


class ChatMessageRequest(BaseModel):
    content: str
    image_urls: list[str] = []


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: str | None = None
