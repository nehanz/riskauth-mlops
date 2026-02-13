from pydantic import BaseModel
from datetime import datetime


class AuthEvent(BaseModel):
    user_id: str
    tenant_id: str
    ip_address: str
    country: str = "Unknown"
    city: str = "Unknown"
    latitude: float = 0.0
    longitude: float = 0.0
    asn: str = "Unknown"
    user_agent: str = "Unknown"
    device_type: str = "desktop"
    rtt: float = 0.0
    login_timestamp: datetime
    login_success: bool = True


class RiskResponse(BaseModel):
    # Risk assessment response
    risk_score: float
    decision: str
