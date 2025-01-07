import streamlit as st

def display_scoreboard():
    if 'agents' not in st.session_state or not st.session_state.agents:
        st.warning("No agents to display.")
        return

    st.subheader("Votes Received by Each Agent")
    votes_summary = {}
    for agent_data in st.session_state.agents:
        name = agent_data['name']
        # If the app was run and agents constructed, they might have a 'votes' attribute in memory,
        # but in this minimal approach, we track them in session state. So we rely on session votes:
        agent_votes_count = 0
        if 'votes' in st.session_state:
            for vote_key in st.session_state.votes:
                # If the vote_key string for that agent is found, increment
                if f"vote_{name}_" in vote_key:
                    agent_votes_count += 1
        votes_summary[name] = agent_votes_count

    sorted_agents = sorted(votes_summary.items(), key=lambda x: x[1], reverse=True)

    for agent_name, vote_count in sorted_agents:
        st.write(f"**{agent_name}**: {vote_count} votes")

    if 'interaction' in st.session_state and st.session_state.interaction:
        st.subheader("Summary Points from Interaction:")
        for idx, item in enumerate(st.session_state.interaction):
            if 'response' in item:
                st.markdown(f"**{item['agent']}** responded: {item['response']}")
            elif 'debate' in item:
                st.markdown(f"**{item['agent']}** debated: {item['debate']}")
    else:
        st.info("No completed interactions to summarize.")
