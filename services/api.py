from fastapi import FastAPI

from riskauth_ml.inference.scorer import score
from riskauth_ml.features.baseline_store import SQLiteBaseline
from .schemas import AuthEvent, RiskResponse
from .logic import make_decision
from storage.event_store import save_event, get_connection

app = FastAPI(
    title="RiskAuth API v2",
    description="Risk-based authentication — 21-feature schema",
    version="2.0.0",
)

# Lazily initialised baseline store (shares events.db)
_baseline_store: SQLiteBaseline | None = None


def _get_baseline_store() -> SQLiteBaseline:
    global _baseline_store
    if _baseline_store is None:
        get_connection()
        _baseline_store = SQLiteBaseline("events.db")
    return _baseline_store


@app.post("/auth-event", response_model=RiskResponse)
def process_auth_event(event: AuthEvent):
    event_dict = event.model_dump()

    # 1. Fetch user baseline
    bs = _get_baseline_store()
    baseline = bs.get(event.user_id)

    # 2. Score
    risk_score = score(event_dict, baseline)

    # 3. Decide
    decision = make_decision(risk_score, event.tenant_id)

    # 4. Persist event
    save_event(event_dict, risk_score, decision)

    # 5. Update baseline
    bs.update(event.user_id, event_dict)

    return RiskResponse(risk_score=risk_score, decision=decision)
