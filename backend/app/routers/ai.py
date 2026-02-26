import base64
import time
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import AIServiceException, NotFoundException
from app.db.database import get_db
from app.models.ai_recognition_log import AIRecognitionLog
from app.models.chat import ChatMessage, ChatSession
from app.models.user import User
from app.schemas.ai import (
    ChatMessageRequest,
    ChatMessageResponse,
    ExerciseRecognitionResponse,
    FoodRecognitionResponse,
    ImageRecognitionRequest,
)
from app.schemas.common import ApiResponse
from app.services.ai import ai_manager
from app.services.ai.prompts import HEALTH_ASSISTANT_SYSTEM_PROMPT

router = APIRouter()


@router.post("/recognize/food", response_model=ApiResponse[FoodRecognitionResponse])
async def recognize_food(
    request: ImageRecognitionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider_name = ai_manager.get_provider_name(current_user.ai_provider)
    provider = ai_manager.get_provider(current_user.ai_provider)

    start_time = time.time()
    try:
        # Fetch image and convert to base64
        import httpx
        async with httpx.AsyncClient() as client:
            img_response = await client.get(request.image_url, timeout=30.0)
            image_base64 = base64.b64encode(img_response.content).decode()

        result = provider.analyze_food_image(image_base64)
        # If provider methods are async
        if hasattr(result, "__await__"):
            result = await result

        processing_time = int((time.time() - start_time) * 1000)

        # Log the recognition
        log = AIRecognitionLog(
            user_id=current_user.id,
            recognition_type="food",
            image_url=request.image_url,
            ai_provider=provider_name,
            parsed_result=result.model_dump(),
            processing_time_ms=processing_time,
        )
        db.add(log)
        await db.flush()

        return ApiResponse(
            data=FoodRecognitionResponse(
                recognition_id=str(log.id),
                foods=[f.model_dump() for f in result.foods],
                total_calories=result.total_calories,
                ai_provider=provider_name,
            )
        )
    except Exception as e:
        raise AIServiceException(f"食物识别失败：{str(e)}")


@router.post("/recognize/exercise", response_model=ApiResponse[ExerciseRecognitionResponse])
async def recognize_exercise(
    request: ImageRecognitionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider_name = ai_manager.get_provider_name(current_user.ai_provider)
    provider = ai_manager.get_provider(current_user.ai_provider)

    start_time = time.time()
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            img_response = await client.get(request.image_url, timeout=30.0)
            image_base64 = base64.b64encode(img_response.content).decode()

        result = provider.analyze_exercise_image(image_base64)
        if hasattr(result, "__await__"):
            result = await result

        processing_time = int((time.time() - start_time) * 1000)

        log = AIRecognitionLog(
            user_id=current_user.id,
            recognition_type="exercise",
            image_url=request.image_url,
            ai_provider=provider_name,
            parsed_result=result.model_dump(),
            processing_time_ms=processing_time,
        )
        db.add(log)
        await db.flush()

        return ApiResponse(
            data=ExerciseRecognitionResponse(
                recognition_id=str(log.id),
                exercise=result.model_dump(),
                ai_provider=provider_name,
            )
        )
    except Exception as e:
        raise AIServiceException(f"运动识别失败：{str(e)}")


@router.post("/recognize/food/upload", response_model=ApiResponse[FoodRecognitionResponse])
async def recognize_food_from_upload(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider_name = ai_manager.get_provider_name(current_user.ai_provider)
    provider = ai_manager.get_provider(current_user.ai_provider)

    start_time = time.time()
    try:
        content = await file.read()
        image_base64 = base64.b64encode(content).decode()

        result = provider.analyze_food_image(image_base64)
        if hasattr(result, "__await__"):
            result = await result

        processing_time = int((time.time() - start_time) * 1000)

        log = AIRecognitionLog(
            user_id=current_user.id,
            recognition_type="food",
            image_url=f"upload:{file.filename}",
            ai_provider=provider_name,
            parsed_result=result.model_dump(),
            processing_time_ms=processing_time,
        )
        db.add(log)
        await db.flush()

        return ApiResponse(
            data=FoodRecognitionResponse(
                recognition_id=str(log.id),
                foods=[f.model_dump() for f in result.foods],
                total_calories=result.total_calories,
                ai_provider=provider_name,
            )
        )
    except Exception as e:
        raise AIServiceException(f"食物识别失败：{str(e)}")


@router.post("/recognize/exercise/upload", response_model=ApiResponse[ExerciseRecognitionResponse])
async def recognize_exercise_from_upload(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider_name = ai_manager.get_provider_name(current_user.ai_provider)
    provider = ai_manager.get_provider(current_user.ai_provider)

    start_time = time.time()
    try:
        content = await file.read()
        image_base64 = base64.b64encode(content).decode()

        result = provider.analyze_exercise_image(image_base64)
        if hasattr(result, "__await__"):
            result = await result

        processing_time = int((time.time() - start_time) * 1000)

        log = AIRecognitionLog(
            user_id=current_user.id,
            recognition_type="exercise",
            image_url=f"upload:{file.filename}",
            ai_provider=provider_name,
            parsed_result=result.model_dump(),
            processing_time_ms=processing_time,
        )
        db.add(log)
        await db.flush()

        return ApiResponse(
            data=ExerciseRecognitionResponse(
                recognition_id=str(log.id),
                exercise=result.model_dump(),
                ai_provider=provider_name,
            )
        )
    except Exception as e:
        raise AIServiceException(f"运动识别失败：{str(e)}")


@router.post("/chat/sessions", response_model=ApiResponse[dict])
async def create_chat_session(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = ChatSession(
        user_id=current_user.id,
        title="新对话",
        ai_provider=ai_manager.get_provider_name(current_user.ai_provider),
    )
    db.add(session)
    await db.flush()
    return ApiResponse(data={"id": str(session.id), "title": session.title})


@router.get("/chat/sessions", response_model=ApiResponse[list[dict]])
async def list_chat_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .where(ChatSession.is_active == True)
        .order_by(ChatSession.updated_at.desc())
    )
    sessions = result.scalars().all()
    return ApiResponse(
        data=[
            {"id": str(s.id), "title": s.title, "updated_at": s.updated_at.isoformat()}
            for s in sessions
        ]
    )


@router.get("/chat/sessions/{session_id}/messages", response_model=ApiResponse[list[ChatMessageResponse]])
async def get_chat_messages(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify session ownership
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session or session.user_id != current_user.id:
        raise NotFoundException("会话不存在")

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()
    return ApiResponse(
        data=[
            ChatMessageResponse(
                role=m.role,
                content=m.content,
                created_at=m.created_at.isoformat() if m.created_at else None,
            )
            for m in messages
        ]
    )


@router.post("/chat/sessions/{session_id}/messages")
async def send_chat_message(
    session_id: uuid.UUID,
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify session
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session or session.user_id != current_user.id:
        raise NotFoundException("会话不存在")

    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=request.content,
        image_urls=request.image_urls if request.image_urls else None,
    )
    db.add(user_msg)
    await db.flush()

    # Build context
    system_prompt = _build_system_prompt(current_user)

    # Get conversation history
    msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    history = [
        {"role": m.role, "content": m.content}
        for m in msg_result.scalars().all()
        if m.role in ("user", "assistant")
    ]

    provider = ai_manager.get_provider(current_user.ai_provider)

    # Stream response via SSE
    async def generate():
        full_response = ""
        try:
            async for chunk in provider.chat_stream(history, system_prompt):
                full_response += chunk
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
        finally:
            # Save assistant message
            assistant_msg = ChatMessage(
                session_id=session_id,
                role="assistant",
                content=full_response,
            )
            db.add(assistant_msg)
            await db.commit()
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.delete("/chat/sessions/{session_id}", response_model=ApiResponse)
async def delete_chat_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session or session.user_id != current_user.id:
        raise NotFoundException("会话不存在")
    session.is_active = False
    await db.flush()
    return ApiResponse(detail="删除成功")


def _build_system_prompt(user: User) -> str:
    user_profile = f"""
- 昵称: {user.nickname}
- 性别: {"男" if user.gender == 1 else "女" if user.gender == 2 else "未知"}
- 身高: {user.height_cm or "未设置"}cm
- 当前体重: {user.current_weight_kg or "未设置"}kg
- 目标体重: {user.target_weight_kg or "未设置"}kg
- 健身目标: {user.fitness_goal or "未设置"}
- 运动水平: {user.activity_level or "未设置"}
- 每日卡路里目标: {user.daily_calorie_target or "未设置"}kcal
"""
    # In production, we would also query recent health data
    health_summary = "暂无近期数据摘要"

    return HEALTH_ASSISTANT_SYSTEM_PROMPT.format(
        user_profile=user_profile,
        health_summary=health_summary,
    )
