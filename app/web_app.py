import asyncio
import os
import re
import sys
import textwrap

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.agents.root_agent import root_agent


load_dotenv()


st.set_page_config(
    page_title="Civic Budget Intelligence",
    page_icon="\U0001F3DB",
    layout="wide",
)


def load_css(file_path: str):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css(os.path.join(PROJECT_ROOT, "app", "static", "style.css"))


# ---------------------------------------------------------------------
# Parse the analysis_agent's final text into fields for the UI card
# ---------------------------------------------------------------------
def parse_agent_output(text: str) -> dict:
    fields = {
        "answer": None,
        "status": None,
        "evidence": None,
        "source": None,
        "page": None,
        "source_file": None,
        "insufficient": False,
        "raw": text,
    }

    if "insufficient to verify" in text.lower():
        fields["insufficient"] = True
        fields["answer"] = text.strip()
        return fields

    patterns = {
        "answer": r"Answer:\s*(.+?)(?=\n\s*Verification Status:|\Z)",
        "status": r"Verification Status:\s*(.+?)(?=\n\s*Supporting Evidence:|\Z)",
        "evidence": r"Supporting Evidence:\s*(.+?)(?=\n\s*Source:|\Z)",
        "source": r"Source:\s*(.+?)(?=\n\s*Page Number:|\Z)",
        "page": r"Page Number:\s*(.+?)(?=\n\s*Source File:|\Z)",
        "source_file": r"Source File:\s*(.+?)(?=\Z)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()

    return fields


def status_class(status: str) -> str:
    if not status:
        return "oga-status-unverified"
    status = status.upper()
    if "PARTIALLY" in status:
        return "oga-status-partial"
    if "CONFLICT" in status:
        return "oga-status-conflicting"
    if "VERIFIED" in status:
        return "oga-status-verified"
    return "oga-status-unverified"


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    st.image(
        os.path.join(PROJECT_ROOT, "app", "static", "logo.png"),
        use_container_width=True,
    )

st.markdown(
    """
    <h1 class="oga-app-title">\U0001F3DB Civic Budget Intelligence</h1>
    <div class="oga-app-subtitle">Research and verification of public budget information</div>
    <div class="oga-badge-wrap">
        <span class="oga-badge">\U0001F4CE Primary source: OpenGov Africa - OGA Budget Lens</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Question card
# ---------------------------------------------------------------------
with st.container(border=True):
    st.markdown("<h3>Ask your question</h3>", unsafe_allow_html=True)

    question = st.text_input(
        "Question",
        placeholder="Example: What did the Kenyan government commit to regarding Universal Health Coverage?",
        label_visibility="collapsed",
    )

    ask_clicked = st.button("\U0001F50E Investigate", type="primary")


# ---------------------------------------------------------------------
# Agent call
# ---------------------------------------------------------------------
async def run_agent(question_text: str):

    runner = InMemoryRunner(
        agent=root_agent,
    )

    user_id = "civic_user"
    session_id = "civic_session"

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=question_text)
        ],
    )

    final_answer = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                text = getattr(part, "text", None)
                if text:
                    print(f"\n--- {event.author} ---\n{text}\n")

        if event.author == "analysis_agent":
            if event.content and event.content.parts:
                for part in event.content.parts:
                    text = getattr(part, "text", None)
                    if text:
                        final_answer = text

    return final_answer


# ---------------------------------------------------------------------
# Results card
# ---------------------------------------------------------------------
if ask_clicked:

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Researching and verifying evidence..."):

            try:
                answer = asyncio.run(run_agent(question.strip()))
            except Exception as exc:
                st.error("The question could not be processed.")
                st.exception(exc)
                answer = None

        if not answer:
            st.warning("No final answer could be generated.")

        else:
            fields = parse_agent_output(answer)

            if fields["insufficient"]:
                html = f"""
<div class="oga-card">
<h3>\U0001F4E3 ANSWER</h3>
<div class="oga-answer-text">{fields['answer']}</div>
</div>
"""
                st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

            else:
                badge_class = status_class(fields["status"])
                status_label = fields["status"] or "UNVERIFIED"
                evidence_html = (fields['evidence'] or 'No evidence available.').replace('\\n', '<br>')

                html = f"""
<div class="oga-card">
<div class="oga-answer-header">
<h3 style="margin-bottom:0;">\U0001F4E3 ANSWER</h3>
<div>
<span style="color:#64748b; font-size:0.85rem; margin-right:8px;">Verification status:</span>
<span class="{badge_class}">{status_label}</span>
</div>
</div>
<div class="oga-answer-text">{fields['answer'] or '—'}</div>
</div>

<div class="oga-card">
<h3>\U0001F5E8 EVIDENCE FOUND</h3>
<div class="oga-evidence-box">{evidence_html}</div>
</div>

<div class="oga-card">
<h3>\U0001F4C4 SOURCE</h3>
<div class="oga-source-grid">
<div class="oga-source-item">
<div class="label">SOURCE</div>
<div class="value">{fields['source'] or '—'}</div>
</div>
<div class="oga-source-item">
<div class="label">PAGE</div>
<div class="value">{fields['page'] or '—'}</div>
</div>
<div class="oga-source-item">
<div class="label">SOURCE FILE</div>
<div class="value">{fields['source_file'] or '—'}</div>
</div>
</div>
</div>
"""
                st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

            if st.button("\U0001F504 New question"):
                st.rerun()
