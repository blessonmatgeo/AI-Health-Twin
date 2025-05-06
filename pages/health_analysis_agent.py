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
st.markdown(
    """
    <style>
    .top-right-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
    }
    </style>
    <a href='Home.py'><button class='top-right-button'>🏠 Back to Home</button></a>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([30, 2])  # Adjust column width to push button to the right
with col2:
    if st.button("🏠"):
        st.switch_page("main_app.py")

st.title("👩‍⚕️ AI Health Twin - Personalized Health Advisor")
st.write("Upload your medical history file (JSON format), and the AI will provide a detailed health analysis.")

# Step 2: File Upload for Health Data
uploaded_file = st.file_uploader("📄 Upload your Health Data file (JSON format):", type=["json"])

# Step 3: Define the Health Analyst Agent
health_analyst_agent = Agent(
    role="Health Data Analyst",
    goal="Analyze patient health metrics and generate a comprehensive health report.",
    backstory="An AI-powered health specialist trained in analyzing patient lifestyle, medical history, and risk factors to generate insightful recommendations.",
    verbose=False,
    memory=True
)

# Step 4: Define the Health Advisor Agent
health_advisor_agent = Agent(
    role="AI Health Advisor",
    goal="Recommend personalized lifestyle changes to optimize health and prevent future diseases.",
    backstory="An AI-driven preventive healthcare expert focusing on personalized diet, exercise, and stress management strategies.",
    verbose=False,
    memory=True
)

# Step 5: Process File Upload & AI Analysis
if st.button("🧑‍⚕️ Get AI Health Analysis"):
    if uploaded_file is None:
        st.error("⚠️ Please upload a valid health data file.")
    else:
        # Read JSON file content
        health_data = json.load(uploaded_file)

        # Define AI Tasks
        health_analysis_task = Task(
            description=f"""
            Analyze the following health data:
            Age: {health_data["age"]}, Gender: {health_data["gender"]}
            Height: {health_data["height"]} cm, Weight: {health_data["weight"]} kg
            Sleep: {health_data["sleep"]} hours, Water Intake: {health_data["water"]} glasses
            Exercise: {health_data["exercise"]}, Diet: {health_data["diet"]}
            Alcohol: {health_data["alcohol"]}, Smoking: {health_data["smoking"]}
            Chronic Conditions: {', '.join(health_data["chronic_conditions"])}
            Family History: {', '.join(health_data["family_history"])}
            Stress Level: {health_data["stress_level"]}/10, Mental Health: {health_data["mental_health"]}
            Medications: {', '.join([med['name'] for med in health_data['medications']])}
            Supplements: {', '.join(health_data['supplements'])}
            Health Goals: {', '.join(health_data['health_goals'])}

            Evaluate key health trends, risks, and potential concerns based on this data.
            """,
            expected_output="A structured report summarizing the health risks, key observations, and insights.",
            agent=health_analyst_agent
        )

        lifestyle_recommendation_task = Task(
            description="""
            Based on the patient's health metrics, provide a personalized lifestyle plan including:
            - Ideal sleep patterns and stress management strategies.
            - Recommended diet based on their chronic conditions.
            - Optimal exercise routine and hydration goals.
            - Preventive measures for risks like diabetes and heart disease.
            """,
            expected_output="A structured health improvement plan with specific, actionable recommendations.",
            agent=health_advisor_agent
        )

        # Create and Run the Crew
        healthcare_crew = Crew(
            agents=[health_analyst_agent, health_advisor_agent],
            tasks=[health_analysis_task, lifestyle_recommendation_task],
            process=Process.sequential
        )

        final_response = healthcare_crew.kickoff(inputs={"health_data": health_data})

        # Convert CrewOutput to string
        health_report_text = str(final_response)

        # Display AI Health Insights
        st.subheader("🤖 AI Health Twin Recommendations:")
        st.success(health_report_text)

        # Save report to file
        with open("health_report.md", "w") as report_file:
            report_file.write(health_report_text)

        # Corrected Download Button
        st.download_button(
            label="📥 Download Full Health Report",
            data=health_report_text.encode("utf-8"),  # Convert to bytes
            file_name="health_report.md",
            mime="text/markdown"
        )
