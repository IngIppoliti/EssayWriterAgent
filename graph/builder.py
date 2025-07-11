from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from models import AgentState
from agents.essaywriter import plan_node, research_plan_node
from agents.essaywriter import generation_node
from agents.essaywriter import reflection_node, research_critique_node
from agents.essaywriter import should_continue

def should_continue(state):
    if state["revision_number"] > state["max_revisions"]:
        return END
    return "reflect"


def build_graph():
    memory = SqliteSaver.from_conn_string(":memory:")
    builder = StateGraph(AgentState)

    builder.add_node("planner", plan_node)
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.add_node("research_plan", research_plan_node)
    builder.add_node("research_critique", research_critique_node)

    builder.set_entry_point("planner")
    builder.add_edge("planner", "research_plan")
    builder.add_edge("research_plan", "generate")
    builder.add_edge("reflect", "research_critique")
    builder.add_edge("research_critique", "generate")
    builder.add_conditional_edges(
        "generate", should_continue, {END: END, "reflect": "reflect"}
    )

    return builder.compile(checkpointer=memory)
