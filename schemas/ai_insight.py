from pydantic import BaseModel

class AIPromptRequest(BaseModel):
    prompt: str
