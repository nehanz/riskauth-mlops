from pydantic import BaseModel
from datetime import datetime


class AuthEvent(BaseModel):
    #Authentication event data
    user_id: str
    tenant_id: str
    ip: str
    device: str
    login_time: datetime


class RiskResponse(BaseModel):
    # Risk assessment response
    risk_score: float
    decision: str
