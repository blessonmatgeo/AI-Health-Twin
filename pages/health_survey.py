import streamlit as st
import json

# Set page title
st.set_page_config(page_title="Health Survey", page_icon="📋", layout="wide")

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
st.title("📋 Health Survey")
st.write("Fill out the form to get a personalized health insight.")

# Basic Information
st.header("Basic Information")
age = st.selectbox("What is your age?", list(range(10, 101)))
gender = st.radio("What is your gender?", ["Male", "Female", "Other"])
height = st.number_input("What is your height? (cm)", min_value=50, max_value=250, step=1)
weight = st.number_input("What is your weight? (kg)", min_value=10, max_value=300, step=1)

# BMI Calculation
bmi = round(weight / ((height / 100) ** 2), 2) if height and weight else None
st.write(f"📊 Your **BMI**: {bmi} (Healthy range: 18.5 - 24.9)" if bmi else "Enter height & weight to calculate BMI.")

# Lifestyle & Daily Habits
st.header("Lifestyle & Daily Habits")
exercise = st.selectbox("How often do you exercise?", ["Never", "1-2 times a week", "3-5 times a week", "Daily"])
st.caption("🏃 Regular exercise reduces heart disease risk by up to 35%!")

sleep = st.selectbox("How many hours of sleep do you get per night?", ["Less than 5", "5-7", "7-9", "More than 9"])
st.caption("🛌 7-9 hours of sleep is ideal for cognitive and physical health.")

water = st.selectbox("How much water do you drink daily? (liters)", ["Less than 1L", "1-2L", "More than 2L"])
st.caption("💧 Drinking 2L of water daily can improve focus and metabolism.")

diet = st.selectbox("How would you describe your daily diet?", ["Balanced", "Mostly Junk", "High in Sugar", "High in Processed Foods", "Vegetarian", "Vegan"])
alcohol = st.radio("Do you consume alcohol?", ["No", "Occasionally", "Frequently"])
smoking = st.radio("Do you smoke?", ["No", "Occasionally", "Yes"])

# Medical History & Risk Factors
st.header("Medical History & Risk Factors")
chronic_conditions = st.multiselect("Do you have any diagnosed chronic conditions?", ["Diabetes", "Hypertension", "Heart Disease", "None"])
allergies = st.radio("Do you have any allergies?", ["Yes", "No"])
family_history = st.multiselect("Does your family have a history of health issues?", ["Diabetes", "Heart disease", "Hypertension", "None"])

# Stress & Mental Well-being
st.header("Stress & Mental Well-being")
stress_level = st.slider("On a scale of 1-10, how would you rate your daily stress levels?", 1, 10, 5)
mental_health = st.radio("Do you experience frequent anxiety or mood swings?", ["Yes", "No", "Occasionally"])

# Medications & Supplements
st.header("Medications & Supplements")
medication_name = st.text_input("Medication Name (if any)", placeholder="E.g., Metformin")
medication_dosage = st.text_input("Dosage", placeholder="E.g., 850mg")
medication_frequency = st.selectbox("Frequency", ["Once a day", "Twice a day", "Weekly", "None"])
supplements = st.text_input("Do you take any supplements?", placeholder="E.g., Vitamin D, Omega-3")

# Health Goals
st.header("Health Goals")
health_goals = st.text_area("What are your health goals?", placeholder="E.g., Improve energy levels, Reduce stress")

# Collect responses into a dictionary
survey_data = {
    "age": age,
    "gender": gender,
    "height": height,
    "weight": weight,
    "bmi": bmi,
    "exercise": exercise,
    "sleep": sleep,
    "water": water,
    "diet": diet,
    "alcohol": alcohol,
    "smoking": smoking,
    "chronic_conditions": chronic_conditions if chronic_conditions else ["None"],
    "allergies": allergies,
    "family_history": family_history if family_history else ["None"],
    "stress_level": stress_level,
    "mental_health": mental_health,
    "medications": [
        {
            "name": medication_name,
            "dosage": medication_dosage,
            "frequency": medication_frequency,
        }
    ] if medication_name else [],
    "supplements": supplements.split(", ") if supplements else [],
    "health_goals": health_goals.split(", ") if health_goals else [],
}

# Ensure all required fields are filled before submission
if st.button("✅ Submit & Download"):
    if not all([age, gender, height, weight, exercise, sleep, water, diet, alcohol, smoking, stress_level, mental_health]):
        st.error("❌ Please fill in all required fields!")
    else:
        json_data = json.dumps(survey_data, indent=4)
        st.download_button(label="📂 Download JSON", data=json_data, file_name="health_survey.json", mime="application/json")
        st.success("✅ Survey successfully completed! Download your responses.")
