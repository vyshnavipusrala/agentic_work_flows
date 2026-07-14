from langgraph.graph import StateGraph, START, END
from agents.state import State
from agents.research_agent import research
from agents.writer_agent import writer
from agents.review_agent import review
from agents.route_agent import route

builder = StateGraph(State)
builder.add_node("research", research)
builder.add_node("writer", writer)
builder.add_node("review", review)
builder.add_node("route", route)
builder.add_edge(START, "route")

def get_next_node(state):
    route = state["next"]
    if route == "research":
        return "research"
    elif route == "writer":
        return "writer"
    elif route == "review":
        return "review"
    else:
        return END

builder.add_conditional_edges(
    "route",
    get_next_node,
    {
        "research": "research",
        "writer": "writer",
        "review": "review",
    }
)
builder.add_edge("research", END)
builder.add_edge("writer", END)
builder.add_edge("review", END)

route_graph = builder.compile()

if __name__ == "__main__":
    topic=input("Enter:")
    result = route_graph.invoke({
        "topic": topic,
        "research_notes": "",
        "article": "",
        "review": "",
        "verdict": "",
        "iteration": 0,
        "next": "",
    })

    if result["next"] == "research":
        print("=== RESEARCH NOTES ===")
        print(result["research_notes"])
    elif result["next"] == "writer":
        print("=== ARTICLE ===")
        print(result["article"])
    elif result["next"] == "review":
        print("=== REVIEWED ARTICLE ===")
        print(result["review"])
    else:
        print("Router returned an unrecognized route — no agent ran.")

    from IPython.display import Image, display

    display(
        Image(
            route_graph.get_graph().draw_mermaid_png()
        )
    )
    png = route_graph.get_graph().draw_mermaid_png()

    with open("Route_graph.png", "wb") as f:
        f.write(png)
