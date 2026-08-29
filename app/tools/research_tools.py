from app.verifier import verify_evidence


def verify_research_evidence(evidence: list) -> dict:
    """
    Verifies a collection of evidence records.

    Use this tool after research has collected evidence
    from one or more independent sources.

    Args:
        evidence: A list of evidence records.

    Returns:
        A verification result containing:
        - status
        - reason
        - evidence
    """

    return verify_evidence(evidence)


def prepare_research_query(query: str) -> dict:
    """
    Prepares a research query for external investigation.

    This tool does not perform web search yet.
    It normalizes the query so that an external
    research source can be connected later.

    Args:
        query: The user's research question.

    Returns:
        A structured research request.
    """

    normalized_query = query.strip()

    return {
        "query": normalized_query,
        "status": "READY_FOR_EXTERNAL_RESEARCH",
    }
