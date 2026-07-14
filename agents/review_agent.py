from langchain_core.messages import HumanMessage,SystemMessage
from agents.llm import model

def review(state):
    topic=state["topic"]
    article=state["article"]
    messages=[
        SystemMessage(
            content="""
      You are an expert content reviewer.

        Your responsibility is to improve the quality of the given article.

    rules:
     -  -Correct the grammer and spelling.
        - Improve the quality.
        - Improve the flow between sections.
        - Keep the article beginner friendly.
        - Don't remove important information
        - Do not add information not present in the research notes.
        - return only the improved article.
"""), 
    HumanMessage(content=f"Review the article about the topic: {topic} based on the following article: {article}")
    ]
    response = model.invoke(messages)
    return { "review": response.content }