import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Set up Streamlit UI
st.set_page_config(page_title="AI Health Educator", layout="wide")

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
st.title("💡 AI Health Educator - Ask Me Anything!")
st.write("Chat with an AI-powered health educator to get answers on general health topics.")

# Step 2: Define the Health Educator Agent
health_educator_agent = Agent(
    role="AI Health Educator",
    goal="Provide accurate, science-backed answers to general health-related questions.",
    backstory=(
        "You are a highly knowledgeable AI health educator with expertise in nutrition, fitness, "
        "mental health, disease prevention, and wellness. You provide reliable, friendly, and easy-to-understand answers."
    ),
    verbose=False,  # Ensures minimal logging
    memory=True  # Keeps track of previous user queries for better context
)

# Step 3: Chat Interface for User Queries
user_query = st.text_input("📝 Ask a health-related question:")

if st.button("💬 Get AI Answer"):
    if user_query.strip() == "":
        st.warning("⚠️ Please enter a health question.")
    else:
        # Define AI Task
        health_education_task = Task(
            description=f"Answer this health-related question in a clear and concise manner: {user_query}",
            expected_output="A well-researched and easy-to-understand answer to the user's health query.",
            agent=health_educator_agent
        )

        # Create a Crew with just the Health Educator
        health_crew = Crew(
            agents=[health_educator_agent],
            tasks=[health_education_task],
            process=Process.sequential
        )

        # Execute Crew to get AI response
        ai_response = health_crew.kickoff()

        # Convert CrewOutput to a clean string
        final_answer = str(ai_response).strip()

        # Display AI's response (Only the final answer)
        st.subheader("🤖 AI Health Educator's Answer:")
        st.write(final_answer)
