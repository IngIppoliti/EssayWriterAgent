from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from models import AgentState
from nodes.planner import plan_node, research_plan_node
from nodes.generator import generation_node
from nodes.reflector import reflection_node, research_critique_node
from nodes.condition import should_continue

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
    builder.add_conditional_edges("generate", should_continue, {END: END, "reflect": "reflect"})

    return builder.compile(checkpointer=memory)
