from google.adk.agents import SequentialAgent

from app.agents.research_agent import research_agent
from app.agents.data_agent import data_agent
from app.agents.verification_agent import verification_agent
from app.agents.provenance_agent import provenance_agent
from app.agents.analysis_agent import analysis_agent


root_agent = SequentialAgent(
    name="civic_budget_intelligence",

    description=(
        "Sequential orchestrator for the Civic Budget Intelligence "
        "multi-agent system."
    ),

    sub_agents=[
        research_agent,
        data_agent,
        verification_agent,
        provenance_agent,
        analysis_agent,
    ],
)