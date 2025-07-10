from graph.builder import build_graph
from IPython.display import Image

def run_app():
    graph = build_graph()
    Image(graph.get_graph().draw_png())
    thread = {"configurable": {"thread_id": "1"}}
    for s in graph.stream({
        'task': "what is the difference between langchain and langsmith",
        "max_revisions": 2,
        "revision_number": 1,
    }, thread):
        print(s)
