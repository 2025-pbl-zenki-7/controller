from pydantic import BaseModel
from enum import Enum


# --- Enum ---


class ConversationStatus(str, Enum):
    ONGOING = "ongoing"
    FINISHED = "finished"
    ERROR = "error"


class ReactionType(str, Enum):
    NEUTRAL = "neutral"
    SURPRISED = "surprised"
    SMILING = "smiling"
    THUMBS_UP = "thumbs_up"
    THINKING = "thinking"
    ANGER = "anger"
    CLAPPING = "clapping"
    UH_HUH = "uh_huh"


class TeaType(str, Enum):
    TEA1 = "tea1"
    TEA2 = "tea2"
    TEA3 = "tea3"


class Amount(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# --- Pydantic ---


class TeaData(BaseModel):
    type: TeaType
    sugar: Amount
    milk: Amount


class AiResponse(BaseModel):
    text: str
    reaction: ReactionType
    status: ConversationStatus
    tea_data: TeaData | None


class UserTextInput(BaseModel):
    text: str
