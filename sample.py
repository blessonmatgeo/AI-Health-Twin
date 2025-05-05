from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool  # Tool for online medical research
from dotenv import load_dotenv

load_dotenv()

# Step 1: Create the Virtual Nurse Agent
nurse_agent = Agent(
    role="Virtual Nurse",
    goal="Assist patients by analyzing symptoms and providing medication reminders.",
    backstory="A friendly and knowledgeable AI nurse who provides symptom insights, medication guidance, and health advice.",
    verbose=True,
    memory=True,  # Enables context retention
    tools=[SerperDevTool()]  # Uses internet search for medical references
)

# Step 2: Get user input
user_symptoms = input("👩‍⚕️ Virtual Nurse: What symptoms are you experiencing? ")
user_medication = input("👩‍⚕️ Virtual Nurse: Are you taking any medications? If so, please enter the name and dosage: ")

# Step 3: Define the Nurse's Tasks
symptom_analysis_task = Task(
    description=f"Analyze the patient's symptoms: {user_symptoms}. "
                "Provide possible causes and recommended next steps (e.g., rest, hydration, or seeing a doctor).",
    expected_output="A summary of symptoms with possible explanations and recommendations.",
    agent=nurse_agent
)

medication_reminder_task = Task(
    description=f"Remind the patient to take {user_medication} at the correct time with proper dosage instructions.",
    expected_output="A medication reminder with dosage details and precautions.",
    agent=nurse_agent
)

# Step 4: Create and Run the Crew
healthcare_crew = Crew(
    agents=[nurse_agent],
    tasks=[symptom_analysis_task, medication_reminder_task],
    process=Process.sequential  # Tasks execute one after the other
)

# Step 5: Execute AI Tasks and Display Results
result = healthcare_crew.kickoff()
print("\n🤖 AI Nurse Response:\n", result)
