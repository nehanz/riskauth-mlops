from fastapi import FastAPI

from riskauth_ml.inference.scorer import score
from .schemas import AuthEvent, RiskResponse
from .logic import make_decision
from storage.event_store import save_event
from policy.tenant_rules import get_rules

app = FastAPI(
    title="RiskAuth API",
    description="Risk-based authentication system",
    version="0.1.0"
)


@app.post("/auth-event", response_model=RiskResponse)
def process_auth_event(event: AuthEvent):
    risk_score = score(event.dict())
    decision = make_decision(risk_score, event.tenant_id)

    save_event(event.dict(), risk_score, decision)

    return RiskResponse(
        risk_score=risk_score,
        decision=decision
    )
