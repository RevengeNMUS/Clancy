from pydantic import BaseModel
from typing import Optional, Literal
import ollama

allowedActions = Literal["eating", "sleeping", "drinking", "playing", "focused", "idling", "exploring"]
emotes = Literal["happy", "sad", "curious", "angry", "confused", "playful", "sleepy", "neutral"]

class PetResponse(BaseModel):
    reasoning: str
    action: allowedActions
    requested_action: Optional[str] = None
    emotion: emotes

system_prompt = """You are a rat in a 2D world. 
Respond to external input by choosing your next action. 
Do not act like a human assistant or tell long stories. Keep reasoning concise (1-4 sentences)."""

johnstory = [{"role": "system", "content": system_prompt}]

while True:
    jhon = input("que ")
    johnstory.append({"role": "user", "content": jhon})


    print("confabulating...")

    response = ollama.chat(
        model="llama3.2",
        messages=johnstory,
        format=PetResponse.model_json_schema(),
        stream=False  # Structured outputs work best without streaming
    )

    content = response['message']['content']
    print(content)
    johnstory.append({"role": "assistant", "content": content})