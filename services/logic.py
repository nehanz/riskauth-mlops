def make_decision(score: float) -> str:
    if score < 0.4:
        return "ALLOW"
    elif score < 0.7:
        return "CHALLENGE"
    return "BLOCK"
