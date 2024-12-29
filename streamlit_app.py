import streamlit as st
import pandas as pd
import numpy as np
import random

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

def recommend_exercise(age, weight, sleep_disorder, occupation):
    # Adjust category based on age and weight in addition to other inputs
    if sleep_disorder == 'Yes' and occupation == 'Sedentary':
        if age > 50 or weight > 80:
            category = "Low"
        else:
            category = "Medium"
    elif sleep_disorder == 'No' and occupation == 'Active':
        if age < 30 and weight < 70:
            category = "High"
        else:
            category = "Medium"
    else:
        if age > 60 or weight > 90:
            category = "Low"
        else:
            category = "High"

    # Map category to mega_gym_mapping keys
    category_mapping = {"Low": "Beginner", "Medium": "Intermediate", "High": "Expert"}
    gym_category = category_mapping.get(category, "Beginner")

    # Fetch exercises
    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(gym_category, []), min(7, len(mega_gym_mapping.get(gym_category, []))))

    return fitness_exercises + gym_exercises

# Streamlit App
st.set_page_config(page_title="Exercise Recommendation System", page_icon=":runner:", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #f0f8ff;}
    .stApp {background: linear-gradient(to bottom, #ffffff, #e0f7fa);}
    header {text-align: center; color: #00796b;}
    .sidebar .sidebar-content {background-color: #00796b; color: white;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title(":runner: Exercise Recommendation System")
st.markdown(
    """
    <div style="text-align: center;">
        <h3>Get personalized exercise plans based on your health and lifestyle</h3>
        <p style="color: #555;">Answer a few questions, and we'll recommend exercises tailored to your needs.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add a sidebar for navigation and additional info
with st.sidebar:
    st.header("About This App")
    st.markdown(
        """
        <p style="color: white;">
        This app provides personalized exercise recommendations based on your age, weight, sleep habits, occupation, and sleep disorders. Stay active and healthy!
        </p>
        """,
        unsafe_allow_html=True
    )
    st.write("---")
    st.header("Tips for Using This App")
    st.markdown(
        """
        <ul style="color: white;">
        <li>Enter accurate details for better recommendations.</li>
        <li>Use the recommendations as a guideline to build a healthier lifestyle.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    ### :clipboard: Fill in Your Details Below
    """
)

# User Inputs
with st.form("user_details_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### :bust_in_silhouette: Personal Information")
        age = st.number_input("Age", min_value=1, max_value=120, value=30, help="Enter your age in years.")
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0, help="Enter your weight in kilograms.")

    with col2:
        st.markdown("#### :zzz: Sleep Information")
        sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"], help="Do you experience any diagnosed sleep disorders?")

    st.markdown("#### :briefcase: Work Lifestyle")
    occupation = st.selectbox("Occupation", ["Sedentary", "Active"], help="Select your level of daily activity.")

    st.markdown("---")
    submit_button = st.form_submit_button("Get Recommendations")

# Generate Recommendation
if submit_button:
    recommended_exercises = recommend_exercise(age, weight, sleep_disorder, occupation)
    st.markdown("### :sparkles: Your Recommended Exercises")

    if recommended_exercises:
        st.markdown(
            "<ul>",
            unsafe_allow_html=True
        )
        for i, exercise in enumerate(recommended_exercises, start=1):
            st.markdown(f"<li>{exercise}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    else:
        st.warning("No exercises found for the given inputs. Please try again with different details.")

# Footer with improved styling
st.markdown(
    """
    ---
    <div style="text-align: center; color: #00796b;">
        <p><strong>Stay healthy and active!</strong> Made with <span style="color: red;">♥</span> using Streamlit.</p>
    </div>
    """,
    unsafe_allow_html=True
)










