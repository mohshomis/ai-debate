import random
from agent import Agent

# Module-level storage of current agents, updated on each call
_agents = []

def propagate_vote(vote_key, agent_name):
    # Let each agent handle the vote signal (e.g., for dynamic strategy)
    for agent in _agents:
        if agent.name == agent_name:
            agent.receive_vote(vote_key)

def perform_interaction(query, agents, num_iterations):
    global _agents
    _agents = agents
    if not agents:
        yield "No agents available."
        return

    # Shuffle to randomize who goes first
    random.shuffle(agents)
    current_response = ""
    previous_agent = None
    previous_response = ""
    conversation_history = []

    for i in range(num_iterations):
        current_agent = agents[i % len(agents)]

        if i == 0:
            # First response to the user query
            current_response = current_agent.generate_response(query)
            yield {"agent": current_agent.name, "response": current_response}
            previous_agent = current_agent
            previous_response = current_response
            conversation_history.append(
                {"speaker": current_agent.name, "text": current_response}
            )
            continue

        # Build conversation for debate
        conversation_history.append(
            {"speaker": previous_agent.name, "text": previous_response}
        )
        debate = current_agent.debate(query, conversation_history)
        yield {"agent": current_agent.name, "debate": debate}
        current_response = debate
        previous_response = current_response
        previous_agent = current_agent
