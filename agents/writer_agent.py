from langchain_core.messages import HumanMessage,SystemMessage
from agents.llm import model

def writer(state):
    topic=state["topic"]
    research_notes=state["research_notes"]
    messages=[
        SystemMessage(
            content="""
    You are a Experienced Writer.
    Who have 30+ years of experience in writing in and out about the given topic.
    
    Your job is to Generate the best article based on the research notes provided.

    Rules:
    -Write a well-structured article.
    - Use headings and subheadings.
    - Only use the research notes provided
    - Do not add any new information
    - Use bullet points
    - Use simple English.
    - Keep the flow logical.
"""), 
    HumanMessage(content=f"Write an article about the topic: {topic} based on the following research notes: {research_notes}")
    ]
    response = model.invoke(messages)
    return { "article": response.content }