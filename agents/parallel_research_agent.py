from langchain_core.messages import HumanMessage, SystemMessage
from agents.llm import model


def parallel_research(state):
    """
    Runs once PER subtopic (dispatched via Send). Each parallel invocation
    receives its own 'task' in state, and appends one entry to research_notes_list.
    """
    task = state["task"]

    messages = [
        SystemMessage(content="""
        You are an experienced research assistant. Given a specific sub-topic, produce
        concise, information-dense research notes on just that sub-topic.

        Rules:
        - Use bullet points
        - Focus only on this sub-topic, do not wander into other areas
        - Do not write an article
        - Do not explain your reasoning
        """),
        HumanMessage(content=f"Research this sub-topic: {task}")
    ]

    response = model.invoke(messages)
    note = f"## {task}\n{response.content}"

    # Returned as a single-item list -- the operator.add reducer on
    # research_notes_list will concatenate this with every other worker's output
    return {"research_notes_list": [note]}

