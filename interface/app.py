from graph.builder import build_graph

# from IPython.display import Image


def run_app():
    print("🔧 Starting EssayWriterAgent...")

    # 🔁 Ricevi sia il grafo compilato che il builder
    graph = build_graph()
    # Image(graph.get_graph().draw_png())

    # 🧠 Esegui thread agent
    thread = {"configurable": {"thread_id": "1"}}
    for s in graph.stream(
        {
            "task": "what is the difference between langchain and langsmith",
            "content": [],
            "max_revisions": 2,
            "revision_number": 1,
        },
        thread,
    ):
        print(s)
