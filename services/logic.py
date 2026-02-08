from policy.tenant_rules import get_rules


def make_decision(score: float, tenant_id: str) -> str:
    rules = get_rules(tenant_id)

    if score < rules["allow_threshold"]:
        return "ALLOW"
    elif score < rules["challenge_threshold"]:
        return "CHALLENGE"
    return "BLOCK"
