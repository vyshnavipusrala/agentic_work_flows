from langchain_core.messages import SystemMessage, HumanMessage
from agents.llm import model


def supervisor(state):
    topic = state["topic"]
    research_notes = state["research_notes"]
    article = state["article"]
    review = state["review"]

    messages = [
        SystemMessage(
            content="""
You are the Supervisor of a team of AI agents.

Available workers:
1. Research Agent
2. Writer Agent
3. Reviewer Agent

Your job is to decide which worker should execute next.

Rules:
- If research_notes is empty -> research
- If research_notes exists but article is empty -> writer
- If article exists but review is empty -> review
- If review exists -> END

Return ONLY one word.

Possible outputs:
research
writer
review
END

Do not explain your answer.
"""
        ),
        HumanMessage(
            content=f"""
Current Workflow State

Topic:
{topic}

Research Notes:
{research_notes}

Article:
{article}

Review:
{review}
"""
        ),
    ]

    response = model.invoke(messages)

    next_step = response.content.strip().lower()

    mapping = {
        "researcher": "research",
        "research": "research",
        "writer": "writer",
        "reviewer": "review",
        "review": "review",
        "end": "END",
    }

    return {
        "next": mapping.get(next_step, "END")
    }