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
st.title("👩‍⚕️ AI Health Twin - Future Health Risk Assessment")
st.write("Upload your health data file (JSON format), and the AI will analyze potential future health risks.")

# Step 2: File Upload for Health Data
uploaded_file = st.file_uploader("📄 Upload your Health Data file (JSON format):", type=["json"])

# Step 3: Define the Risk Assessment Agent
risk_assessment_agent = Agent(
    role="Health Risk Specialist",
    goal="Analyze patient health data and predict potential future risks.",
    backstory="An AI-powered medical expert trained to identify potential health risks based on current health metrics, medical history, and lifestyle habits.",
    verbose=False,
    memory=True
)

# Step 4: Define the Preventive Care Agent
preventive_care_agent = Agent(
    role="Preventive Health Advisor",
    goal="Recommend proactive health measures to reduce future risks.",
    backstory="An AI-driven preventive care expert specializing in early disease prevention through lifestyle modifications and routine monitoring.",
    verbose=False,
    memory=True
)

# Step 5: Process File Upload & AI Analysis
if st.button("🔬 Analyze Future Health Risks"):
    if uploaded_file is None:
        st.error("⚠️ Please upload a valid JSON health data file.")
    else:
        # Read JSON file contents
        health_data = json.load(uploaded_file)

        # Define AI Tasks
        risk_analysis_task = Task(
            description=f"""
            Based on the patient's health data, analyze and outline possible future health risks.
            Consider the following factors:
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

            Predict potential future health risks based on trends in their data.
            Identify diseases or conditions they may be susceptible to over time.
            """,
            expected_output="A detailed health risk assessment report listing potential future health risks and explanations.",
            agent=risk_assessment_agent
        )

        preventive_care_task = Task(
            description="""
            Based on the predicted health risks, provide actionable preventive measures.
            Suggest lifestyle adjustments, dietary improvements, medical check-ups, and fitness routines
            to reduce the likelihood of future health issues.
            """,
            expected_output="A structured preventive care guide with clear steps to reduce health risks.",
            agent=preventive_care_agent
        )

        # Create and Run the Crew
        healthcare_crew = Crew(
            agents=[risk_assessment_agent, preventive_care_agent],
            tasks=[risk_analysis_task, preventive_care_task],
            process=Process.sequential  # Tasks execute one after another
        )

        final_response = healthcare_crew.kickoff(inputs={"health_data": health_data})

        # Convert CrewOutput to string
        health_risk_report = str(final_response)

        # Display AI Health Risk Assessment
        st.subheader("🩺 AI Health Risk Prediction:")
        st.write(health_risk_report)
