from fastapi import FastAPI

from riskauth_ml.inference.scorer import score
from .schemas import AuthEvent, RiskResponse
from .logic import make_decision


app = FastAPI(
    title="RiskAuth API",
    description="Risk-based authentication system",
    version="0.1.0"
)


@app.post("/auth-event", response_model=RiskResponse)
def process_auth_event(event: AuthEvent):
    risk_score = score(event.dict())
    decision = make_decision(risk_score)

    return RiskResponse(
        risk_score=risk_score,
        decision=decision
    )
