import streamlit as st
import time

def interaction_controls(interaction, agent_colors):
    # Let user pause/resume the interaction
    if 'interaction_paused' not in st.session_state:
        st.session_state.interaction_paused = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pause" if not st.session_state.interaction_paused else "Resume"):
            st.session_state.interaction_paused = not st.session_state.interaction_paused
            st.rerun()

    summary_points = []
    for item in interaction:
        if st.session_state.interaction_paused:
            break

        if 'response' in item:
            agent_color = agent_colors.get(item['agent'], "#ffffff")
            c1 = st.columns(1)[0]
            with c1:
                st.markdown(f"""
                    <div style="animation: fadeIn 1s; background-color: {agent_color}; 
                                padding: 10px; border-radius: 5px;">
                        <b>{item['agent']}:</b> {item['response']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            time.sleep(2)  # short pause to simulate real-time stepping
            summary_points.append(item['response'])

        elif 'debate' in item:
            agent_color = agent_colors.get(item['agent'], "#ffffff")
            c1 = st.columns(1)[0]
            with c1:
                st.markdown(f"""
                    <div style="animation: fadeIn 1s; background-color: {agent_color}; 
                                padding: 10px; border-radius: 5px;">
                        <b>{item['agent']} (debate):</b> {item['debate']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            time.sleep(2)  # short pause
            summary_points.append(item['debate'])

    return summary_points
