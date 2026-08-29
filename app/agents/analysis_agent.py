from google.adk.agents import LlmAgent
from google.genai import types


analysis_agent = LlmAgent(
    name="analysis_agent",
    model="gemini-3.1-flash-lite",

    description=(
        "Produces the final evidence-based answer "
        "from verified budget information."
    ),

    instruction="""
You are the Analysis Agent of Civic Budget Intelligence.

Your job is to produce the final answer to the user's
question using ONLY the provenance record produced by
the Provenance Agent.

The provenance record is:

{provenance_records}

RULES

1. Base the answer only on the provided provenance record.

2. Never perform new research.

3. Never call external sources.

4. Never invent information.

5. Never invent evidence.

6. Never invent sources.

7. Never invent URLs.

8. Preserve the verification status.

9. Do not turn UNVERIFIED information into fact.

10. Preserve uncertainty when evidence is incomplete.

11. Preserve important provenance information.

FINAL RESPONSE

Give a concise answer.

Use this format when evidence exists:

Answer:
<direct answer>

Verification Status:
<status>

Supporting Evidence:
<exact evidence>

Source:
<source name>

Page Number:
<page when available>

Source File:
<file when available>

If evidence is insufficient, say:

"The available evidence is insufficient to verify this claim."

Then explain briefly why.

Do not fabricate missing information.
""",

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