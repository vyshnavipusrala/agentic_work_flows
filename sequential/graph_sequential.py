from langgraph.graph import StateGraph, START, END
from agents.state import State
from agents.research_agent import research
from agents.writer_agent import writer
from agents.review_agent import review

builder = StateGraph(State)

builder.add_node("research", research)
builder.add_node("writer", writer)
builder.add_node("review", review)

builder.add_edge(START, "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", "review")
builder.add_edge("review", END)

graph = builder.compile()

if __name__ == "__main__":
    topic=input("Enter the topic you want to research: ")
    result = graph.invoke({
        "topic": topic,
        "research_notes": "",
        "article": "",
        "review": "",
        "verdict": "",
        "iteration": 0,
    })

    print("=== RESEARCH NOTES ===")
    print(result["research_notes"])
    print("\n=== ARTICLE (before review) ===")
    print(result["article"])
    print("\n=== FINAL REVIEWED ARTICLE ===")
    print(result["review"])

    from IPython.display import Image, display

    display(
        Image(
            graph.get_graph().draw_mermaid_png()
        )
    )
    png = graph.get_graph().draw_mermaid_png()

    with open("Sequential_graph.png", "wb") as f:
        f.write(png)