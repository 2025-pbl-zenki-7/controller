from google import genai
from google.genai import types
import dotenv

from schemas import (
    AiResponse,
)

from instruction_prompt import system_instruction


API_KEY = dotenv.get_key(".env", "GEMINI_API_KEY")


class CafeOwner:
    def __init__(self):
        self.__client = genai.Client(api_key=API_KEY)
        self.__model = "gemini-1.5-flash"
        self.__config = types.GenerateContentConfig(
            # thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="application/json",
            response_schema=AiResponse,
            system_instruction=system_instruction,
        )
        self.__chat = self.__client.chats.create(
            model=self.__model,
            config=self.__config,
        )

    def input(self, text: str):
        response = self.__chat.send_message(text)
        print(response.text)
        print(response.parsed)
        output = AiResponse(
            text=response.parsed.text,
            reaction=response.parsed.reaction,
            status=response.parsed.status,
            tea_data=response.parsed.tea_data,
        )
        return output


# ai = CafeOwner()

# while True:
#    ai.input(input())
