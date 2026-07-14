from langchain_core.messages import SystemMessage, HumanMessage
from agents.llm import model


def route(state):
    input = state['topic']
    message = [
        SystemMessage(content="""
            Your an Expert in categorizing prompts.
            Your job is very important that after analysis of user prompt.
            you need to decide , this comes in which section.
            we have 3 types of sections:
            1. researcher
            2. writer
            3. reviewer
            you just need to generate among this
            Rules:
            - No reasoning needed
            - One one word solution
            Example
            user: Research the history of Agentic AI.
            you: researcher
            user: Convert these notes into an article.
            you: writer
            user: Improve grammar and clarity of this article.
            you: reviewer
            ok like this only one word answer
            """),
        HumanMessage(content=f"\n'User Topic is \n{input}'")
    ]
    response = model.invoke(message)
    route = response.content.strip().lower()
    mapping = {
        "researcher": "research",
        "research": "research",
        "writer": "writer",
        "reviewer": "review",
        "review": "review",
    }
    normalized = mapping.get(route, route)


    return {
        "next": normalized
    }