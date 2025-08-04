from fastapi import APIRouter, WebSocket, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from instruction_prompt import instruction_config
from schemas import TeaTypeConfig


from schemas import AiResponse, ConversationStatus

from ai import CafeOwner

conversation_router = APIRouter(
    prefix="/api/conversation",
    tags=["conversation"],
)

admin_router = APIRouter(prefix="/api/admin", tags=["admin"])


cafe_owner = CafeOwner()


# ----- Conversation Routers -----


@conversation_router.get("/start", summary="Start a conversation")
async def start_conversation():
    cafe_owner.refresh()


@conversation_router.websocket("/communicate")
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
        print("An error occured at websocket_communicate()")
        print(f"Error: {e}")

    finally:
        print("WebSocket connection closed.")
        pass


# ----- Admin Routers -----


@admin_router.get("/", response_class=HTMLResponse)
async def admin_page(request: Request):
    templates = Jinja2Templates(directory="./templates/")
    return templates.TemplateResponse(name="admin.html", request=request)


@admin_router.get("/update/teatype", response_class=HTMLResponse)
async def update_teatype(tea1: str, tea2: str, tea3: str, request: Request):
    if tea1 and tea2 and tea3:
        teaTypes = TeaTypeConfig(tea1=tea1, tea2=tea2, tea3=tea3)
        instruction_config.tea_type = teaTypes

    templates = Jinja2Templates(directory="./templates/")
    return templates.TemplateResponse(name="admin.html", request=request)
