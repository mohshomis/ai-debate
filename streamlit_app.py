import streamlit as st
import time
from backend import perform_interaction, Agent

st.title("AI Agent Interaction")

if 'page' not in st.session_state:
    st.session_state.page = "main"

if 'num_iterations' not in st.session_state:
    st.session_state.num_iterations = 3

if st.sidebar.button("Settings"):
    st.session_state.page = "settings"

@st.cache_resource
def get_agent_manager():
    return []

if 'agents' not in st.session_state:
    st.session_state.agents = get_agent_manager()

if st.session_state.page == "main":
    st.header("Interaction")
    user_query = st.text_input("Enter your query:")
    if st.button("Start Interaction"):
        if 'agents' in st.session_state and st.session_state.agents:
            agents = [Agent(**agent_data) for agent_data in st.session_state.agents]
            agents = [Agent(**agent_data) for agent_data in st.session_state.agents]
            interaction = perform_interaction(user_query, agents, st.session_state.num_iterations)
            placeholder = st.empty()
            summary_points = []
            colors = ["#f0f8ff", "#f0ffff", "#f5f5dc", "#f8f8ff", "#f0fff0", "#fffaf0", "#f5fffa", "#fff0f5", "#faf0e6", "#ffefd5"]
            agent_colors = {}
            for i, agent_data in enumerate(agents):
                agent_colors[agent_data.name] = colors[i % len(colors)]
            for item in interaction:
                if 'response' in item:
                    agent_color = agent_colors[item['agent']]
                    st.markdown(f"""
                        <div style="animation: fadeIn 1s; background-color: {agent_color}; padding: 10px; border-radius: 5px;">
                            <b>{item['agent']}:</b> {item['response']}
                        </div>
                        """, unsafe_allow_html=True)
                    summary_points.append(item['response'])
                elif 'debate' in item:
                    agent_color = agent_colors[item['agent']]
                    st.markdown(f"""
                        <div style="animation: fadeIn 1s; background-color: {agent_color}; padding: 10px; border-radius: 5px;">
                            <b>{item['agent']} (debate):</b> {item['debate']}
                        </div>
                        """, unsafe_allow_html=True)
                    summary_points.append(item['debate'])
                time.sleep(1)
            # final_summary_points = [f"**{item['agent']}:** {item['debate']}" for item in interaction if 'debate' in item]
            # final_summary = "<ul>" + "".join([f"<li>{point}</li>" for point in final_summary_points]) + "</ul>"
            # st.subheader("Final Summary")
            # st.markdown(f"""
            #     <style>
            #     @keyframes fadeIn {{
            #         from {{ opacity: 0; }}
            #         to {{ opacity: 1; }}
            #     }}
            #     </style>
            #     {final_summary}
            # """, unsafe_allow_html=True)
        else:
            st.warning("Please add agents in the settings page.")

elif st.session_state.page == "settings":
    st.header("Settings")
    if st.button("Back to Home"):
        st.session_state.page = "main"

    with st.expander("Interaction Settings", expanded=True):
        num_iterations = st.number_input("Number of Iterations", min_value=1, max_value=10, value=st.session_state.num_iterations, step=1)
        if st.button("Save Iterations"):
            st.session_state.num_iterations = num_iterations

    with st.expander("Add New Agent", expanded=True):
        new_agent_name = st.text_input("Agent Name")
        new_agent_api_key = st.text_input("API Key")
        new_agent_company = st.selectbox("Company", ["OpenAI", "Anthropic", "Gemini"])
        if new_agent_company == "OpenAI":
            new_agent_model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"])
        elif new_agent_company == "Anthropic":
            new_agent_model = st.selectbox("Model", ["claude-2", "claude-instant-1"])
        elif new_agent_company == "Gemini":
            new_agent_model = st.selectbox("Model", ["gemini-pro", "gemini-ultra"])
        else:
            new_agent_model = st.text_input("Model")
        
        new_agent_character_preset = st.selectbox("Character Preset", ["Scientist", "Politician", "Historian", "Philosopher", "Journalist", "Custom"])
        new_agent_character_custom = st.text_input("Custom Character Description", disabled=(new_agent_character_preset != "Custom"))

        if st.button("Add Agent"):
            if not new_agent_name:
                st.error("Agent name cannot be empty.")
            else:
                if new_agent_character_preset == "Custom":
                    new_agent_character = new_agent_character_custom
                else:
                    new_agent_character = new_agent_character_preset
                new_agent = {"name": new_agent_name, "api_key": new_agent_api_key, "company": new_agent_company, "model": new_agent_model, "character": new_agent_character}
                st.session_state.agents.append(new_agent)
                st.success(f"Agent '{new_agent_name}' added!")

    if st.session_state.agents:
        st.subheader("Existing Agents")
        for i, agent in enumerate(st.session_state.agents):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{agent['name']}** ({agent['company']} - {agent['model']})")
            with col2:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.edit_index = i
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    del st.session_state.agents[i]
                    st.experimental_rerun()

    if 'edit_index' in st.session_state:
        with st.expander(f"Edit Agent: {st.session_state.agents[st.session_state.edit_index]['name']}", expanded=True):
            edit_agent_name = st.text_input("Agent Name", value=st.session_state.agents[st.session_state.edit_index]['name'])
            edit_agent_api_key = st.text_input("API Key", value=st.session_state.agents[st.session_state.edit_index]['api_key'])
            edit_agent_company = st.selectbox("Company", ["OpenAI", "Anthropic", "Gemini"], index=["OpenAI", "Anthropic", "Gemini"].index(st.session_state.agents[st.session_state.edit_index]['company']))
            if edit_agent_company == "OpenAI":
                edit_agent_model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"], index=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"].index(st.session_state.agents[st.session_state.edit_index]['model']))
            elif edit_agent_company == "Anthropic":
                edit_agent_model = st.selectbox("Model", ["claude-2", "claude-instant-1"], index=["claude-2", "claude-instant-1"].index(st.session_state.agents[st.session_state.edit_index]['model']))
            elif edit_agent_company == "Gemini":
                edit_agent_model = st.selectbox("Model", ["gemini-pro", "gemini-ultra"], index=["gemini-pro", "gemini-ultra"].index(st.session_state.agents[st.session_state.edit_index]['model']))
            else:
                edit_agent_model = st.text_input("Model", value=st.session_state.agents[st.session_state.edit_index]['model'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes"):
                    if not edit_agent_name:
                        st.error("Agent name cannot be empty.")
                    elif not edit_agent_api_key:
                        st.error("API Key cannot be empty.")
                    elif not edit_agent_model:
                        st.error("Model cannot be empty.")
                    else:
                        st.session_state.agents[st.session_state.edit_index]['name'] = edit_agent_name
                        st.session_state.agents[st.session_state.edit_index]['api_key'] = edit_agent_api_key
                        st.session_state.agents[st.session_state.edit_index]['company'] = edit_agent_company
                        st.session_state.agents[st.session_state.edit_index]['model'] = edit_agent_model
                        del st.session_state.edit_index
                        st.experimental_rerun()
            with col2:
                if st.button("Cancel"):
                    del st.session_state.edit_index
    st.markdown("---")
    st.markdown("Developed by Mohammed Shomis")
