
from typing import Callable, List
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode


def create_tool_calling_agent(llm, system_promt:str, agent_name: str, tools: List[Callable], call_after_tool: bool = True):
    llm_with_tools = llm.bind_tools(tools)

    def agent (state, config):
        llm_response = llm_with_tools.invoke([SystemMessage(system_promt)] + state["messages"])
        llm_response.name = agent_name
        # invoke agent
        state['messages'].append(llm_response)

        # if tool calls detected invoke the tools
        if(tools_condition(state) == 'tools'):
            tool_node = ToolNode(tools)
            response = tool_node.invoke(state)

            for tool_message in response['messages']:
                state['messages'].append(tool_message)
                if tool_message.artifact:
                    state={**state, **tool_message.artifact}

            if call_after_tool :
                agent(state, config)
            else :
                return state
            
        return state

    return agent