import asyncio
from fastapi import APIRouter, WebSocket, HTTPException, status
from fastapi.encoders import jsonable_encoder
import json

from schemas import (
    AiResponse,
    ConversationStatus,
    UserTextInput,
    ReactionType,
)

from ai import CafeOwner

router = APIRouter(
    prefix="/api/conversation",
    tags=["conversation"],
)


cafe_owner = CafeOwner()


@router.get("/start", summary="Start a conversation")
async def start_conversation():
    cafe_owner = CafeOwner()


@router.websocket("/communicate")
async def websocket_communicate(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # UI --> API (User's input)
            received_data = await websocket.receive_json()

            user_text: str = received_data.get("text", "")

            response: AiResponse = cafe_owner.input(user_text)

            # API --> UI (AI's response)
            await websocket.send_json(jsonable_encoder(response))

            if response.status == ConversationStatus.FINISHED:
                break

    except Exception as e:
        print(f"An error occured at websocket_communicate()")
        print(f"Error: {e}")

    finally:
        print("WebSocket connection closed.")
        pass
