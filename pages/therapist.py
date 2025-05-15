import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Set up Streamlit UI
st.set_page_config(page_title="AI Therapist", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;} /* Hides default Streamlit sidebar navigation */
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<h1 class="centered">👨‍⚕️ AI Health Twin</h1>', unsafe_allow_html=True)
# Sidebar Navigation Buttons
st.sidebar.page_link("main_app.py", label="🏠 Home")
st.sidebar.page_link("pages/health_analysis_agent.py", label="🩺 Health Analysis")
st.sidebar.page_link("pages/lifestyle_coach_agent.py", label="🏋️‍♂️ Lifestyle Recommendations")
st.sidebar.page_link("pages/health_educator.py", label="📖 General Educator")
st.sidebar.page_link("pages/risk_factor_agent.py", label="⚠️ Risk Factor Detection")
st.sidebar.page_link("pages/therapist.py", label="💙 Emotional Support")

# Add a small footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 AI Health Twin | Your Digital Health Companion")
col1, col2 = st.columns([30, 2])  # Adjust column width to push button to the right
with col2:
    if st.button("🏠"):
        st.switch_page("main_app.py")
st.title("🧠 AI Therapist - Your Virtual Mental Health Companion")
st.write("Chat with a friendly, non-judgmental AI therapist about stress, motivation, and well-being.")

# Step 2: Define the AI Therapist Agent
therapist_agent = Agent(
    role="AI Therapist",
    goal="Provide empathetic, supportive, and helpful mental health conversations.",
    backstory=(
        "You are a compassionate and understanding AI therapist. You provide emotional support, "
        "help users manage stress, and encourage self-care practices. You are not a substitute for a professional therapist, "
        "but you offer thoughtful advice and encouragement."
    ),
    verbose=False,  # Ensures a clean, conversational experience
    memory=True  # Enables conversational flow and remembering past responses
)

# Step 3: Chat Interface for User Conversations
user_input = st.text_input("💬 Share your thoughts or ask for advice:")

if st.button("🗣️ Talk to AI Therapist"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter something to start the conversation.")
    else:
        # Define AI Task
        therapy_session_task = Task(
            description=f"Engage in a supportive, empathetic conversation. The user says: {user_input}",
            expected_output="A warm, thoughtful, and encouraging response that fosters emotional well-being.",
            agent=therapist_agent
        )

        # Create a Crew with the AI Therapist
        therapy_crew = Crew(
            agents=[therapist_agent],
            tasks=[therapy_session_task],
            process=Process.sequential
        )

        # Execute Crew to get AI response
        ai_response = therapy_crew.kickoff()

        # Convert CrewOutput to a clean string
        final_answer = str(ai_response).strip()

        # Display AI's response
        st.subheader("🤖 AI Therapist's Response:")
        st.write(final_answer)
