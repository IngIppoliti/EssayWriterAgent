from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an essay. \
Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes \
or instructions for the sections."""

WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 5-paragraph essays.\
Generate the best essay possible for the user's request and the initial outline. \
If the user provides critique, respond with a revised version of your previous attempts. \
Utilize all the information below as needed: 

------

{content}"""

#generate eventually a critique
REFLECTION_PROMPT = """You are a teacher grading an essay submission. \
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, depth, style, etc."""


RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can \
be used when writing the following essay. Generate a list of search queries that will gather \
any relevant information. Only generate 3 queries max."""

#after a critique generate a list of search queries
RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can \
be used when making any requested revisions (as outlined below). \
Generate a list of search queries that will gather any relevant information. Only generate 3 queries max."""



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
