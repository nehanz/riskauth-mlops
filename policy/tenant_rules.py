TENANT_RULES = {
    "tenantA": {
        "allow_threshold": 0.3,
        "challenge_threshold": 0.6
    },
    "tenantB": {
        "allow_threshold": 0.5,
        "challenge_threshold": 0.8
    }
}

DEFAULT_RULES = {
    "allow_threshold": 0.4,
    "challenge_threshold": 0.7
}


def get_rules(tenant_id: str) -> dict:
    return TENANT_RULES.get(tenant_id, DEFAULT_RULES)
