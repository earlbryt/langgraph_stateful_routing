from typing import Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from create_agent import create_tool_calling_agent
from greeting_agent import greeting_agent_prompt, redirect_tool
from sign_up_agent import sign_up_prompt, sign_up_tool
from report_agent import report_agent_prompt, save_report_tool
from langgraph.graph import MessagesState


GREETING_AGENT = "Greeting_Agent"
REPORT_AGENT = "Report_Agent"
SIGN_UP_AGENT = "Sign_up_agent"

# Define the agent state to track the conversation
class AgentState(MessagesState):
    current_route: str
    first_name: str
    last_name: str
    email: str
    reports: list[str]

# Routs to the last agent.
def pre_greeting_routing (default_route: str):
    def routing (state:AgentState) -> str :
        # Route to the last used agent, if it exists in the state
        if 'current_route' in state and state['current_route']:
            print("Routing to " + state['current_route'])
            return state['current_route']
        else:
            # Default to the Greeting Agent if no last agent is found
            return default_route
    
    return routing

# Routes to a selected agent.
def post_greeting_routing (default_route: str):
    def routing (state:AgentState) -> str :
        if 'current_route' not in state or state['current_route'] == GREETING_AGENT:
            return default_route
        elif 'current_route' in state and state['current_route']:
            print("Routing to " + state['current_route'])
            return state['current_route']
       
    return routing

llm = ChatOpenAI(model="gpt-4o")

sign_up_agent = create_tool_calling_agent(llm, sign_up_prompt, SIGN_UP_AGENT, [sign_up_tool(GREETING_AGENT)])
report_agent = create_tool_calling_agent(llm, report_agent_prompt, REPORT_AGENT, [save_report_tool(GREETING_AGENT)])
greeting_agent = create_tool_calling_agent(llm, greeting_agent_prompt(
    {   
        SIGN_UP_AGENT: "Can open an account for the user.",
        REPORT_AGENT: "Can report an issue.",
    }
), GREETING_AGENT, [redirect_tool], call_after_tool=False) 

# Build graph
builder = StateGraph(AgentState)
builder.add_conditional_edges(
    START,
    pre_greeting_routing(GREETING_AGENT),
)

builder.add_node(GREETING_AGENT, greeting_agent)
builder.add_conditional_edges(
    GREETING_AGENT,
    post_greeting_routing(END),
)

builder.add_node(SIGN_UP_AGENT, sign_up_agent)
builder.add_node(REPORT_AGENT, report_agent)

memory = MemorySaver()
# Compile graph
graph = builder.compile(checkpointer=memory)

# from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))