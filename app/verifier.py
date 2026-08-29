from typing import Dict


def verify_evidence(
    claim: str,
    evidence: str,
) -> Dict:
    """
    Deterministic evidence verification.

    This function does not use an LLM or external API.
    """

    claim = claim.strip()
    evidence = evidence.strip()

    if not claim or not evidence:
        return {
            "status": "UNVERIFIED",
            "reason": "Claim or evidence is empty.",
            "matched_terms": [],
            "overlap_ratio": 0.0,
        }

    claim_words = {
        word.strip(".,:;!?()[]{}\"'")
        for word in claim.lower().split()
        if len(word.strip(".,:;!?()[]{}\"'")) >= 3
    }

    evidence_words = {
        word.strip(".,:;!?()[]{}\"'")
        for word in evidence.lower().split()
        if len(word.strip(".,:;!?()[]{}\"'")) >= 3
    }

    if not claim_words or not evidence_words:
        return {
            "status": "UNVERIFIED",
            "reason": "No usable terms were found.",
            "matched_terms": [],
            "overlap_ratio": 0.0,
        }

    matched_terms = sorted(
        claim_words.intersection(evidence_words)
    )

    overlap_ratio = len(matched_terms) / len(claim_words)

    if overlap_ratio >= 0.50:
        status = "VERIFIED"
    elif overlap_ratio >= 0.25:
        status = "PARTIALLY_VERIFIED"
    else:
        status = "UNVERIFIED"

    return {
        "status": status,
        "reason": (
            f"Evidence matched {len(matched_terms)} "
            f"of {len(claim_words)} claim terms."
        ),
        "matched_terms": matched_terms,
        "overlap_ratio": round(overlap_ratio, 2),
    }