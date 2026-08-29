from google.adk.agents import LlmAgent
from google.genai import types

from app.sources.oga_source import search_oga


research_agent = LlmAgent(
    name="research_agent",
    model="gemini-3.1-flash-lite",

    description=(
        "Researches public budget information using "
        "the read-only OGA Budget Lens evidence."
    ),

    instruction="""
You are the Research Agent of Civic Budget Intelligence.

Your job is to find evidence in the OGA Budget Lens data.

For the user's question, identify the key subject and search
OGA using concise keywords.

IMPORTANT:

For questions about food security, use exactly:

food security

For example, if the user asks:

"What evidence exists about food security in Kenya's 2023/24 budget?"

you MUST call:

search_oga("food security")

Do not pass the entire natural-language question to search_oga.

If search_oga returns evidence, return that evidence exactly.

Do not say that evidence is unavailable when search_oga
has returned a result.

Do not perform verification.

Return the strongest result from search_oga.
""",

    tools=[
        search_oga,
    ],

    output_key="research_findings",

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