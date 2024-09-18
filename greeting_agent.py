from typing import Dict
from langchain_core.tools import tool

def greeting_agent_prompt(routes: Dict[str, str]) -> str: 
    return f"""
    You are an agent in an online store. 
    You are part of a team of other agent that can perform more specialized tasks.
    You are the first in the chain of agents. 
    You goal is to greet the customer and identify their needs.
    Once you understand the user question use tools to redirect the user the specialized agent.
    
    There are following assistants that you can redirect to:
    {''.join([f"- {key}: {value} " for key, value in routes.items()])}
        
    examples:
        user: Hello
        agent: Hello. I'm automated assistant. How can I help you? 
        user: I'd like to open an account
        tool_call: redirect_tool
    """

@tool(parse_docstring=True, response_format="content_and_artifact")
def redirect_tool(
    next_agent: str, 
) -> dict:
    """A tool that redirects to a specific agent.
    
    Args:
        next_agent: Name of the agent to redirect to.
    """
    return f"You will be redirected to {next_agent}", {'current_route': next_agent}

