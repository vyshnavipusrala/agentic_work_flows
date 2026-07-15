from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    topic: str
    task: str                                              # NEW: single subtopic, set per-branch by Send
    tasks: list[str]                                        # NEW: full list from splitter
    research_notes_list: Annotated[list[str], operator.add]  # NEW: accumulates one note per worker
    research_notes: str                                     # existing: final joined string
    article: str
    review: str
    verdict: str
    iteration: int
    route: str
    next: str

