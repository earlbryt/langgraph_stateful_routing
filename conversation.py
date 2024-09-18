# Simulate running the graph with a dynamic conversation
from stateful_routing import AgentState
from langchain_core.messages import HumanMessage
from stateful_routing import graph

def simulate_conversation(user_input_sequence, thread_id):
    # Initialize the state with an empty message list
    state = AgentState(messages=[], current_agnet=None)
    
    for user_input in user_input_sequence:
        # Add the user's input as a message to the state
        state['messages'].append(HumanMessage(content=user_input, name="User"))
        
        messagesBefore = len(state['messages'])

        print(f"User: {user_input}")
        # Run the conversation through the graph
        state = graph.invoke(state, {'configurable': {"thread_id":thread_id}})

        newMessages = state['messages'][messagesBefore:]
    
        for response in newMessages:
            if 'tool_calls' in response.additional_kwargs:   
                for call in response.additional_kwargs['tool_calls']:  
                    print(f"({type(response).__name__}) {call['function']['name']}: {call['function']['arguments']}")
            else : 
                print(f"({type(response).__name__}) {response.name} : {response.content}")
            
            
        
    print("================")


# Example conversation sequence
user_inputs = [
    "Hello",
    "I'd like to submit an issue",  # Done with passport, move to car plate
    "My internet is very slow",
    "I can just say that youtube is not working",
    "thank you"
]

simulate_conversation(user_inputs, "cccc")