
from langchain_core.tools import tool

def sign_up_tool(return_route:str):
    
    @tool(parse_docstring=True, response_format="content_and_artifact")
    def tool_func(first_name: str, last_name: str, email: str):
        """Saves user first and last name.
        
        Args:
            first_name : user first name
            last_name : user last name
            email : user email
        """
        print("CREATING USER" , first_name, last_name, email)
        
        return "User signed up. Verification email is sent", {
            'current_route': return_route, 
            'first_name': first_name, 
            'last_name': last_name, 
            'email': email
            }
    
    return tool_func


sign_up_prompt = f"""
You are the assistant that signs up a user. 
You need to collect user name, last name, and email and save it using tools
"""
