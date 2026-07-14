from langgraph.graph import StateGraph, START, END

from agents.state import State
from agents.supervisor_agent import supervisor
from agents.research_agent import research
from agents.writer_agent import writer
from agents.review_agent import review


# Create Graph
builder = StateGraph(State)

# Add Nodes
builder.add_node("supervisor", supervisor)
builder.add_node("research", research)
builder.add_node("writer", writer)
builder.add_node("review", review)

# Start with Supervisor
builder.add_edge(START, "supervisor")


# Router Function
def route(state: State):
    return state["next"]


# Supervisor decides which worker to execute
builder.add_conditional_edges(
    "supervisor",
    route,
    {
        "research": "research",
        "writer": "writer",
        "review": "review",
        "END": END,
    },
)

# Every worker returns control to Supervisor
builder.add_edge("research", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("review", "supervisor")


# Compile Graph
graph = builder.compile()

if __name__ == "__main__":
    from IPython.display import Image, display


    topic = input("Enter Topic: ")

    result = graph.invoke(
        {
            "topic": topic,
            "research_notes": "",
            "article": "",
            "review": "",
            "verdict": "",
            "iteration": 0,
            "next": "",
        }
    )

    print("\n==============================")
    print("WORKFLOW COMPLETED")
    print("==============================")

    if result["research_notes"]:
        print("\n===== RESEARCH NOTES =====")
        print(result["research_notes"])

    if result["article"]:
        print("\n===== ARTICLE =====")
        print(result["article"])

    if result["review"]:
        print("\n===== REVIEWED ARTICLE =====")
        print(result["review"])

    # Save graph image
    png = graph.get_graph().draw_mermaid_png()

    with open("supervisor_graph.png", "wb") as f:
        f.write(png)

    # Display graph (works in Jupyter/Colab)
    try:
        display(Image(png))
    except:
        pass


