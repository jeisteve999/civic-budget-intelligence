from datetime import datetime, timezone


def create_evidence(
    source_name: str,
    source_url: str,
    claim: str,
    evidence: str,
    source_type: str = "unknown",
) -> dict:
    """
    Create a traceable evidence record.
    """

    return {
        "claim": claim,
        "evidence": evidence,
        "source": {
            "name": source_name,
            "url": source_url,
            "type": source_type,
        },
        "retrieved_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }