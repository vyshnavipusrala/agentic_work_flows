from langchain_core.messages import HumanMessage, SystemMessage
from agents.llm import model
 
 
def splitter(state):
    topic = state["topic"]
 
    messages = [
        SystemMessage(content="""
        You are a research planner. Given a broad topic, break it down into 3 to 5
        smaller, distinct sub-topics that together cover the topic well.
        
        Rules:
        - Each sub-topic should be a short phrase (not a full sentence)
        - Sub-topics should not overlap much with each other
        - Output ONLY the sub-topics, one per line
        - No numbering, no bullets, no extra commentary
        """),
        HumanMessage(content=f"Break down this topic: {topic}")
    ]
 
    response = model.invoke(messages)
 
    # Turn the LLM's line-per-subtopic output into a clean list
    tasks = [
        line.strip()
        for line in response.content.splitlines()
        if line.strip()
    ]
 
    return {"tasks": tasks}