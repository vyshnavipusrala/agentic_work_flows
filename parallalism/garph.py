from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from agents.state import State
from agents.splitter_agent import splitter
from agents.parallel_research_agent import parallel_research
from agents.join_agent import join
from agents.writer_agent import writer
from agents.review_agent import review


def fan_out_to_workers(state):
    """
    Called right after splitter. Returns a list of Send objects --
    one per subtopic -- so LangGraph spawns that many parallel
    research invocations, each with its own 'task' in state.
    """
    return [
        Send("parallel_research", {"topic": state["topic"], "task": task})
        for task in state["tasks"]
    ]


builder = StateGraph(State)

builder.add_node("splitter", splitter)
builder.add_node("parallel_research", parallel_research)
builder.add_node("join", join)
builder.add_node("writer", writer)
builder.add_node("review", review)

builder.add_edge(START, "splitter")

# Dynamic fan-out: splitter -> N parallel research_worker branches
builder.add_conditional_edges("splitter", fan_out_to_workers, ["parallel_research"])

# Fan-in: join waits for ALL parallel_research branches to finish
builder.add_edge("parallel_research", "join")

builder.add_edge("join", "writer")
builder.add_edge("writer", "review")
builder.add_edge("review", END)

parallel_graph = builder.compile()

if __name__ == "__main__":
    topic = input("Enter topic: ")
    result = parallel_graph.invoke({
        "topic": topic,
        "task": "",
        "tasks": [],
        "research_notes_list": [],
        "research_notes": "",
        "article": "",
        "review": "",
        "verdict": "",
        "iteration": 0,
        "route": "",
        "next": "",
    })

    print("\n=== SUBTOPICS ===")
    for t in result["tasks"]:
        print("-", t)
    print("\n=== MERGED RESEARCH NOTES ===")
    print(result["research_notes"])
    print("\n=== ARTICLE ===")
    print(result["article"])
    print("\n=== REVIEWED ARTICLE ===")
    print(result["review"])

    from IPython.display import Image, display

    display(
        Image(
            parallel_graph.get_graph().draw_mermaid_png()
        )
    )

    png=parallel_graph.get_graph().draw_mermaid_png()

    with open("parallel_graph.png", "wb") as f:
        f.write(png)



