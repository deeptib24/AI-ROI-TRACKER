from pydantic import BaseModel

class AIRequestCreate(BaseModel):
    feature_name: str
    model_name: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency: float

class PromptRequest(BaseModel):
    feature_name: str
    prompt: str
    engagement_score: float
    retention_score: float