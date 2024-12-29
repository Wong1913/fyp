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
    "High": fitness_mapping.get('High', []) + mega_gym_mapping.get('Advanced', [])
}

def recommend_exercise(age, weight, sleep_duration, occupation, sleep_disorder):
    # Map occupation and sleep disorder to categories
    if sleep_disorder == 'Yes' and occupation == 'Sedentary':
        category = "Low"
    elif sleep_disorder == 'No' and occupation == 'Active':
        category = "Medium"
    else:
        category = "High"
    
    # Map category to mega_gym_mapping keys
    category_mapping = {"Low": "Beginner", "Medium": "Intermediate", "High": "Advanced"}
    gym_category = category_mapping.get(category, "Beginner")

    # Fetch exercises
    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(gym_category, []), min(7, len(mega_gym_mapping.get(gym_category, []))))

    return fitness_exercises + gym_exercises

# Streamlit App
st.set_page_config(page_title="Exercise Recommendation System", layout="centered")
st.title(":runner: Exercise Recommendation System")
st.markdown(
    """
    ### Provide your details to get personalized exercise recommendations
    Fill in the form below, and our system will recommend exercises tailored to your lifestyle and health needs.
    """
)

# User Inputs
with st.form("user_details_form"):
    age = st.number_input("Age", min_value=1, max_value=120, value=30, help="Enter your age in years.")
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0, help="Enter your weight in kilograms.")
    sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0, help="How many hours of sleep do you get on average?")
    occupation = st.selectbox("Occupation", ["Sedentary", "Active"], help="Select your level of daily activity.")
    sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"], help="Do you experience any diagnosed sleep disorders?")
    submit_button = st.form_submit_button("Get Recommendations")

# Generate Recommendation
if submit_button:
    recommended_exercises = recommend_exercise(age, weight, sleep_duration, occupation, sleep_disorder)
    st.markdown("### :sparkles: Your Recommended Exercises:")
    
    if recommended_exercises:
        for i, exercise in enumerate(recommended_exercises, start=1):
            st.markdown(f"**{i}.** {exercise}")
    else:
        st.warning("No exercises found for the given inputs. Please try again with different details.")

# Footer
st.markdown(
    """
    ---
    Made with :heart: using Streamlit. Stay healthy and active! :muscle:
    """
)  









