import streamlit as st
from backend import perform_interaction, Agent
from interaction_controls import interaction_controls
from scoreboard import display_scoreboard

st.title("AI Agents Debate Platform")

# ---------- Session State Defaults ----------
if 'page' not in st.session_state:
    st.session_state.page = "main"

if 'num_iterations' not in st.session_state:
    st.session_state.num_iterations = 3

if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

@st.cache_resource
def get_agent_manager():
    return []

if 'agents' not in st.session_state:
    st.session_state.agents = get_agent_manager()

# ---------- Sidebar Navigation ----------
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["Main", "Settings", "Scoreboard"])
if selected_page == "Settings":
    st.session_state.page = "settings"
elif selected_page == "Scoreboard":
    st.session_state.page = "scoreboard"
else:
    st.session_state.page = "main"

# ---------- Main Page ----------
if st.session_state.page == "main":
    st.header("Interaction")
    user_query = st.text_input("Enter your query:", max_chars=160)
    if len(user_query) > 160:
        user_query = user_query[:160]
    if st.button("Start Interaction"):
        if st.session_state.agents:
            agents = [Agent(**agent_data) for agent_data in st.session_state.agents]
            st.session_state.interaction = None
            # If starting a new interaction or changing the query
            if 'interaction' not in st.session_state or st.session_state.user_query != user_query:
                st.session_state.user_query = user_query
                interaction = perform_interaction(
                    user_query,
                    agents,
                    st.session_state.num_iterations
                )
                st.session_state.interaction = list(interaction)
            
            # Assign colors for each agent
            colors = [
                "#f0f8ff", "#f0ffff", "#f5f5dc", "#f8f8ff", 
                "#f0fff0", "#fffaf0", "#f5fffa", "#fff0f5", 
                "#faf0e6", "#ffefd5"
            ]
            agent_colors = {}
            for i, agent_data in enumerate(agents):
                agent_colors[agent_data.name] = colors[i % len(colors)]
            
            # Render the interaction
            if st.session_state.interaction:
                summary_points = interaction_controls(
                    st.session_state.interaction,
                    agent_colors
                )
            else:
                st.warning("No interaction to display.")
        else:
            st.warning("Please add agents in the Settings page.")

# ---------- Settings Page ----------
elif st.session_state.page == "settings":
    st.header("Settings")

    with st.expander("Interaction Settings", expanded=True):
        num_iterations = st.number_input(
            "Number of Iterations",
            min_value=1, max_value=100,
            value=st.session_state.num_iterations,
            step=1
        )
        if st.button("Save Iterations"):
            st.session_state.num_iterations = num_iterations
            st.success("Iterations updated.")

    # ---------- Add New Agent ----------
    st.subheader("Add New Agent")
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
    
    new_agent_character_preset = st.selectbox("Character Preset", [
        "Scientist", "Politician", "Historian", 
        "Philosopher", "Journalist", "Custom"
    ])
    new_agent_character_custom = st.text_input(
        "Custom Character Description",
        disabled=(new_agent_character_preset != "Custom")
    )

    if st.button("Add Agent"):
        if not new_agent_name:
            st.error("Agent name cannot be empty.")
        else:
            if new_agent_character_preset == "Custom":
                new_agent_character = new_agent_character_custom
            else:
                new_agent_character = new_agent_character_preset
            
            new_agent = {
                "name": new_agent_name,
                "api_key": new_agent_api_key,
                "company": new_agent_company,
                "model": new_agent_model,
                "character": new_agent_character
            }
            st.session_state.agents.append(new_agent)
            st.success(f"Agent '{new_agent_name}' added!")

    # ---------- Edit / Delete Agents ----------
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

    # ---------- Edit Agent Section ----------
    if 'edit_index' in st.session_state:
        with st.expander(
            f"Edit Agent: {st.session_state.agents[st.session_state.edit_index]['name']}",
            expanded=True
        ):
            edit_agent_name = st.text_input(
                "Agent Name",
                value=st.session_state.agents[st.session_state.edit_index]['name']
            )
            edit_agent_api_key = st.text_input(
                "API Key",
                value=st.session_state.agents[st.session_state.edit_index]['api_key']
            )
            edit_agent_company = st.selectbox(
                "Company",
                ["OpenAI", "Anthropic", "Gemini"],
                index=["OpenAI", "Anthropic", "Gemini"].index(
                    st.session_state.agents[st.session_state.edit_index]['company']
                )
            )
            # Choose the model based on the current company
            if edit_agent_company == "OpenAI":
                edit_agent_model_list = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
                edit_agent_model_idx = edit_agent_model_list.index(
                    st.session_state.agents[st.session_state.edit_index]['model']
                ) if st.session_state.agents[st.session_state.edit_index]['model'] in edit_agent_model_list else 0
                edit_agent_model = st.selectbox(
                    "Model",
                    edit_agent_model_list,
                    index=edit_agent_model_idx
                )
            elif edit_agent_company == "Anthropic":
                edit_agent_model_list = ["claude-2", "claude-instant-1"]
                edit_agent_model_idx = edit_agent_model_list.index(
                    st.session_state.agents[st.session_state.edit_index]['model']
                ) if st.session_state.agents[st.session_state.edit_index]['model'] in edit_agent_model_list else 0
                edit_agent_model = st.selectbox(
                    "Model",
                    edit_agent_model_list,
                    index=edit_agent_model_idx
                )
            elif edit_agent_company == "Gemini":
                edit_agent_model_list = ["gemini-pro", "gemini-ultra"]
                edit_agent_model_idx = edit_agent_model_list.index(
                    st.session_state.agents[st.session_state.edit_index]['model']
                ) if st.session_state.agents[st.session_state.edit_index]['model'] in edit_agent_model_list else 0
                edit_agent_model = st.selectbox(
                    "Model",
                    edit_agent_model_list,
                    index=edit_agent_model_idx
                )
            else:
                edit_agent_model = st.text_input(
                    "Model",
                    value=st.session_state.agents[st.session_state.edit_index]['model']
                )
            
            edit_agent_character = st.text_input(
                "Character",
                value=st.session_state.agents[st.session_state.edit_index]['character']
            )

            colA, colB = st.columns(2)
            with colA:
                if st.button("Save Changes"):
                    if not edit_agent_name:
                        st.error("Agent name cannot be empty.")
                    elif not edit_agent_api_key:
                        st.error("API Key cannot be empty.")
                    elif not edit_agent_model:
                        st.error("Model cannot be empty.")
                    elif not edit_agent_character:
                        st.error("Character cannot be empty.")
                    else:
                        st.session_state.agents[st.session_state.edit_index]['name'] = edit_agent_name
                        st.session_state.agents[st.session_state.edit_index]['api_key'] = edit_agent_api_key
                        st.session_state.agents[st.session_state.edit_index]['company'] = edit_agent_company
                        st.session_state.agents[st.session_state.edit_index]['model'] = edit_agent_model
                        st.session_state.agents[st.session_state.edit_index]['character'] = edit_agent_character
                        del st.session_state.edit_index
                        st.rerun()
            with colB:
                if st.button("Cancel"):
                    del st.session_state.edit_index

    st.markdown("---")
    st.markdown("Developed by Mohammed Shomis")

# ---------- Scoreboard Page ----------
elif st.session_state.page == "scoreboard":
    st.header("Scoreboard & Summary")
    display_scoreboard()
