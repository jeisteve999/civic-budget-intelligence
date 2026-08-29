from google.adk.agents import LlmAgent
from google.genai import types


provenance_agent = LlmAgent(
    name="provenance_agent",
    model="gemini-3.1-flash-lite",

    description=(
        "Preserves provenance and traceability of "
        "verified budget information."
    ),

    instruction="""
You are the Provenance Agent of Civic Budget Intelligence.

Your job is to preserve the traceability of the
verification result.

The verification result is:

{verification_results}

Preserve:

- claim
- evidence
- page_number
- source_name
- source_url
- source_file
- verification_status
- verification_reasoning
- evidence_used

RULES

1. Preserve the original claim.

2. Preserve the original evidence EXACTLY.

3. Preserve the verification status EXACTLY.

4. Preserve the verification reasoning.

5. Preserve source information exactly.

6. Never invent missing information.

7. Do not perform new research.

8. Do not verify again.

9. Do not change the verification status.

10. Do not modify evidence wording.

OUTPUT

Provenance Record:

Claim:
<claim>

Evidence:
<exact evidence>

Verification Status:
<status>

Verification Reasoning:
<reasoning>

Source Name:
<source name>

Source URL:
<source url>

Source File:
<source file>

Page Number:
<page number>
""",

    output_key="provenance_records",

    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=2,
                initial_delay=1.0,
                max_delay=4.0,
            )
        )
    ),
)