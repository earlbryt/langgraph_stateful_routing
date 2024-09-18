from langchain_core.tools import tool

def save_report_tool(return_route:str):
    @tool(parse_docstring=True, response_format="content_and_artifact")
    def tool_func(issue: str) -> str:
        """Saves an issue reported by the user.
        
        Args:
            issue: Summary of the issue reported by the user
        """
        print("Tool Call: save_report_tool", issue)
        
        return "report is submited", {'current_route': return_route, 'reports': [issue]}

    return tool_func


report_agent_prompt = f"""ou are the assistant who receives a report about an issue. 
Ask the user to describe an issue. Once done use the tools available to save it.
Example:
User: My internet is very slow
Assistant: I\'m sorry to hear that. Can you please provide me with more details about the issue?
User: I can not tell you much. Youtube is just not working.
Assistant: Thank you for the information. Have notified the support team.
"""
