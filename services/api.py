from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from riskauth_ml.inference.scorer import score


app = FastAPI(title="RiskAuth API")

# Request & Response Schemas
class AuthEvent(BaseModel):
    user_id: str
    tenant_id: str
    ip: str
    device: str
    login_time: datetime


class RiskResponse(BaseModel):
    risk_score: float
    decision: str

# Policy Engine
def make_decision(score: float) -> str:
    if score < 0.4:
        return "ALLOW"
    elif score < 0.7:
        return "CHALLENGE"
    return "BLOCK"

# FIRST ENDPOINT
@app.post("/auth-event", response_model=RiskResponse)
def process_auth_event(event: AuthEvent):
    risk_score = score(event.dict())
    decision = make_decision(risk_score)

    return RiskResponse(
        risk_score=risk_score,
        decision=decision
    )
