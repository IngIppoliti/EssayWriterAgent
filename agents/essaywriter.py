from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


#take the task in input and generate a plan (to build the essay chapter, sections, structure)
def plan_node(state: AgentState):
    messages = [
        SystemMessage(content=PLAN_PROMPT), 
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    return {"plan": response.content}


#AGENT that take the OUTLINE AND PERFORM EXTRACT SOME QUERIES 
def research_plan_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([              #to force that the output will be something with a structure (in this case the object Queries)
        SystemMessage(content=RESEARCH_PLAN_PROMPT),
        HumanMessage(content=state['task'])                               #it's a task for which the agent will research the query
    ])
    content = state['content'] or []                                      #we look the list of documents if there is the node content in the output otherwise we create an empty list
    for q in queries.queries:                                             #we loop over the queries we generated
        response = tavily.search(query=q, max_results=2)                  #we run the queries into Tavily
        for r in response['results']:                                     #we put each response from each queries in the content
            content.append(r['content'])
    return {"content": content}


#AGENT WRITER that take the task and the content and write the essay
def generation_node(state: AgentState):
    content = "\n\n".join(state['content'] or [])
    user_message = HumanMessage(
        content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
    messages = [
        SystemMessage(
            content=WRITER_PROMPT.format(content=content)
        ),
        user_message
        ]
    response = model.invoke(messages)
    return {
        "draft": response.content, 
        "revision_number": state.get("revision_number", 1) + 1
    }


#AGENT that writhe the CRITIQUE
def reflection_node(state: AgentState):
    messages = [
        SystemMessage(content=REFLECTION_PROMPT), 
        HumanMessage(content=state['draft'])
    ]
    response = model.invoke(messages)
    return {"critique": response.content}


#AGENT CRITIQUE RESEARCHER that perform researches on the critique that has been done and add them to the content
def research_critique_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
        HumanMessage(content=state['critique'])
    ])
    content = state['content'] or []
    for q in queries.queries:
        response = tavily.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])
    return {"content": content}


def should_continue(state):
    if state["revision_number"] > state["max_revisions"]:
        return END
    return "reflect"


