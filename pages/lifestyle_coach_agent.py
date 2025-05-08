import streamlit as st
import json
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Set up Streamlit UI
st.set_page_config(page_title="AI Health Twin", layout="wide")

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
st.title("👩‍⚕️ AI Health Twin - Lifestyle Coach")
st.write("Upload your health data file (JSON format), and the AI will provide personalized lifestyle recommendations.")

# Step 2: File Upload for Health Data
uploaded_file = st.file_uploader("📄 Upload your Health Data file (JSON format):", type=["json"])

# Step 3: Define the Health Analysis Agent
health_analysis_agent = Agent(
    role="Health Data Analyst",
    goal="Assess health metrics and suggest improvements for better well-being.",
    backstory="An AI-driven health specialist focused on analyzing patient data and identifying areas of improvement.",
    verbose=False,
    memory=True
)

# Step 4: Define the Lifestyle Optimization Agent
lifestyle_coach_agent = Agent(
    role="AI Lifestyle Coach",
    goal="Recommend practical, actionable lifestyle changes for better health.",
    backstory="An AI expert in preventive healthcare, fitness, and nutrition, dedicated to guiding individuals towards healthier living.",
    verbose=False,
    memory=True
)

# Step 5: Process File Upload & AI Analysis
if st.button("🧑‍⚕️ Get AI Health Recommendations"):
    if uploaded_file is None:
        st.error("⚠️ Please upload a valid JSON health data file.")
    else:
        # Read JSON file contents
        health_data = json.load(uploaded_file)

        # Define AI Tasks
        health_analysis_task = Task(
            description=f"""
            Analyze the following health data:
            - Age: {health_data["age"]}, Gender: {health_data["gender"]}
            - Height: {health_data["height"]} cm, Weight: {health_data["weight"]} kg
            - Sleep: {health_data["sleep"]} hours, Water Intake: {health_data["water"]} glasses
            - Exercise: {health_data["exercise"]}, Diet: {health_data["diet"]}
            - Alcohol: {health_data["alcohol"]}, Smoking: {health_data["smoking"]}
            - Chronic Conditions: {', '.join(health_data["chronic_conditions"])}
            - Family History: {', '.join(health_data["family_history"])}
            - Stress Level: {health_data["stress_level"]}/10, Mental Health: {health_data["mental_health"]}
            - Medications: {', '.join([med['name'] for med in health_data['medications']])}
            - Supplements: {', '.join(health_data['supplements'])}
            - Health Goals: {', '.join(health_data['health_goals'])}

            Identify potential health risks, trends, and areas that need improvement.
            """,
            expected_output="A structured analysis of current health status and improvement areas.",
            agent=health_analysis_agent
        )

        lifestyle_recommendation_task = Task(
            description="""
            Based on the patient's health metrics, suggest specific lifestyle changes to enhance well-being.
            Provide actionable recommendations on:
            - **Optimizing Sleep:** Suggested duration and quality improvement tips.
            - **Dietary Adjustments:** Foods to include/avoid based on chronic conditions.
            - **Exercise Routine:** Best fitness practices for their health goals.
            - **Stress Management:** Techniques to reduce stress and improve mental well-being.
            - **Preventive Care:** Long-term habits to maintain a healthy lifestyle.
            """,
            expected_output="A structured lifestyle plan with detailed, actionable steps to improve overall health.",
            agent=lifestyle_coach_agent
        )

        # Create and Run the Crew
        healthcare_crew = Crew(
            agents=[health_analysis_agent, lifestyle_coach_agent],
            tasks=[health_analysis_task, lifestyle_recommendation_task],
            process=Process.sequential  # Tasks execute one after another
        )

        final_response = healthcare_crew.kickoff(inputs={"health_data": health_data})

        # Convert CrewOutput to string
        health_recommendations = str(final_response)

        # Display AI Health Insights
        st.subheader("🤖 AI Health Twin Recommendations:")
        st.write(health_recommendations)
