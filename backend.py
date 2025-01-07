import random
from agent import Agent

def get_random_agent(agents):
    return random.choice(agents)

def perform_interaction(query, agents, num_iterations):
    if not agents:
        yield "No agents available."
        return

    random.shuffle(agents)
    current_response = ""
    previous_agent = None
    previous_response = ""
    conversation_history = []

    for i in range(num_iterations):
        current_agent = agents[i % len(agents)]

        if i == 0:
            current_response = current_agent.generate_response(query)
            yield {"agent": current_agent.name, "response": current_response}
            previous_agent = current_agent
            previous_response = current_response
            conversation_history.append({"speaker": current_agent.name, "text": current_response})
            continue

        conversation_history.append({"speaker": previous_agent.name, "text": previous_response})
        debate = current_agent.debate(query, conversation_history)
        yield {"agent": current_agent.name, "debate": debate}
        current_response = debate
        previous_response = current_response
        previous_agent = current_agent
