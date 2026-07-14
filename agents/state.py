from typing import TypedDict

class State(TypedDict):
    topic: str
    research_notes: str
    article: str
    review: str
    verdict: str
    iteration: int
    next: str

