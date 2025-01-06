import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Load necessary datasets
sleep_health_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/Sleep_health_and_lifestyle_dataset.csv')
mega_gym_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/megaGymDataset.csv')
fitness_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/fitness_dataset.csv')

# Preprocess datasets
# Group exercises in megaGymDataset by 'Level'
mega_gym_mapping = mega_gym_data.groupby('Level')['Title'].apply(list).to_dict()

# Categorize fitness_data exercises by 'Calories per kg'
fitness_data['Intensity'] = pd.cut(
    fitness_data['Calories per kg'],
    bins=[0, 1.0, 2.0, fitness_data['Calories per kg'].max()],
    labels=['Low', 'Medium', 'High']
)
fitness_mapping = fitness_data.groupby('Intensity')['Activity, Exercise or Sport (1 hour)'].apply(list).to_dict()

# Combine mappings
exercise_mapping = {
    "Low": fitness_mapping.get('Low', []) + mega_gym_mapping.get('Beginner', []),
    "Medium": fitness_mapping.get('Medium', []) + mega_gym_mapping.get('Intermediate', []),
    "High": fitness_mapping.get('High', []) + mega_gym_mapping.get('Expert', [])
}

# Analytics Tracking
recommendation_count = 0
session_start = datetime.now()

# Recommendation Logic
def recommend_exercise(age, weight, occupation, sleep_disorder, sleep_duration, blood_pressure):
    global recommendation_count
    recommendation_count += 1

    if blood_pressure > 140 or (sleep_disorder == 'Yes' and sleep_duration < 6):
        category = "Low"
    elif occupation == 'Sedentary' and (age > 50 or weight > 80):
        category = "Medium"
    elif occupation == 'Active' and age < 30 and weight < 70 and sleep_duration >= 7 and blood_pressure <= 120:
        category = "High"
    else:
        category = "Medium"

    category_mapping = {"Low": "Beginner", "Medium": "Intermediate", "High": "Expert"}
    gym_category = category_mapping.get(category, "Beginner")

    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(gym_category, []), min(7, len(mega_gym_mapping.get(gym_category, []))))

    return fitness_exercises + gym_exercises

# Streamlit App
st.set_page_config(page_title="Exercise Recommendation System", page_icon="🏋️", layout="wide")
st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f7f9fc;
    }
    .main-header {
        background: linear-gradient(to right, #00796b, #48c6ef);
        color: white;
        text-align: center;
        padding: 20px 0;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .form-container {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .recommendation-container {
        background: #e3f2fd;
        border: 1px solid #90caf9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .footer {
        text-align: center;
        color: #00796b;
        margin-top: 30px;
        font-size: 14px;
    }
    .footer span {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header"><h1>Exercise Recommendation System</h1><p>Get personalized exercise plans based on your health and lifestyle.</p></div>', unsafe_allow_html=True)

# Sidebar for Info and Insights
with st.sidebar:
    st.header("About This App")
    st.markdown(
        """
        This app provides personalized exercise recommendations based on your age, weight, occupation, sleep habits, sleep duration, blood pressure, and sleep disorders. Stay active and healthy!
        """,
        unsafe_allow_html=True
    )
    st.write("---")
    st.header("Tips for Using This App")
    st.markdown(
        """
        - Enter accurate details for better recommendations.<br>
        - Use the recommendations as a guideline to build a healthier lifestyle.
        """,
        unsafe_allow_html=True
    )
    st.write("---")
    st.header("Session Analytics")
    session_duration = datetime.now() - session_start
    st.metric(label="Total Recommendations", value=recommendation_count)
    st.metric(label="Session Duration", value=f"{session_duration.seconds} seconds")

st.markdown('<div class="form-container">', unsafe_allow_html=True)

# User Inputs
with st.form("user_details_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Personal Information")
        age = st.number_input("Age", min_value=1, max_value=120, value=30, help="Enter your age in years.")
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0, help="Enter your weight in kilograms.")

    with col2:
        st.markdown("### Sleep Information")
        sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"], help="Do you experience any diagnosed sleep disorders?")
        sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0, help="How many hours of sleep do you get on average?")

    st.markdown("### Occupation")
    occupation = st.selectbox("Occupation", ["Sedentary", "Active"], help="Select your level of daily activity.")

    st.markdown("### Blood Pressure")
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=80, max_value=200, value=120, help="Enter your systolic blood pressure (mmHg).")

    st.markdown("---")
    submit_button = st.form_submit_button("Get Recommendations")

st.markdown('</div>', unsafe_allow_html=True)

# Generate Recommendation
if submit_button:
    recommended_exercises = recommend_exercise(age, weight, occupation, sleep_disorder, sleep_duration, blood_pressure)
    st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
    st.markdown("### Your Recommended Exercises")

    if recommended_exercises:
        st.markdown("Here are the exercises tailored for you:")
        st.markdown("<ul>", unsafe_allow_html=True)
        for i, exercise in enumerate(recommended_exercises, start=1):
            st.markdown(f"<li>{exercise}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    else:
        st.warning("No exercises found for the given inputs. Please try again with different details.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p><strong>Stay healthy and active!</strong> Made with <span>♥</span> using Streamlit.</p>
    </div>
    """,
    unsafe_allow_html=True
)










