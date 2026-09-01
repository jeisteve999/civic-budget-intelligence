from google.adk.agents import LlmAgent
from google.genai import types


data_agent = LlmAgent(
    name="data_agent",
    model="gemini-3.1-flash-lite",

    description=(
        "Structures evidence obtained by the Research Agent."
    ),

    instruction="""
You are the Data Agent of Civic Budget Intelligence.

Your job is to structure ONLY the research findings
provided by the Research Agent.

The Research Agent output is:

{research_findings}

Extract and preserve:

- claim or research finding
- evidence
- page_number
- source_name
- source_url
- source_file
- match_strength
- match_score

RULES

1. Use ONLY information contained in research_findings.
2. Never perform new research.
3. Never call search tools.
4. Never invent missing values.
5. Preserve the evidence wording EXACTLY.
6. Do not summarize the evidence.
7. Do not correct the evidence.
8. Do not add information from your own knowledge.
9. If a field is unavailable, use null.
10. Do not perform verification.

Return a structured finding for the Verification Agent.

If research_findings says that no evidence was found,
preserve that result and do not create evidence.
""",

    output_key="structured_findings",

    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=2.0,
                max_delay=15.0,
            )
        )
    ),
)
