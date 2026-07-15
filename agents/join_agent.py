from langchain_core.messages import HumanMessage, SystemMessage
from agents.llm import model


def join(state):
    """
    Runs once, after ALL parallel research_worker branches have finished.
    Uses the LLM to synthesize the list of per-subtopic notes into one
    coherent set of research notes for writer to use.
    """
    notes_list = state.get("research_notes_list", [])
    combined_raw = "\n\n".join(notes_list)

    messages = [
        SystemMessage(content="""
            You are a research synthesizer. Given a list of research notes covering
            different sub-topics, integrate them into a single, unified set of research notes.

            Rules:
            - Only keep information that is directly relevant to the overall topic
            - Remove duplicate or overlapping points across sub-topics
            - Preserve all distinct facts -- do not drop unique information
            - Keep the notes in bullet-point form (not prose, not an article)
            - Output ONLY the merged research notes, no extra commentary
            """),
        HumanMessage(content=f"Research notes to integrate:\n\n{combined_raw}")
    ]

    response = model.invoke(messages)
    return {"research_notes": response.content}