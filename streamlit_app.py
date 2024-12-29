import streamlit as st
import pandas as pd
import numpy as np
import random

# Load necessary datasets
sleep_health_data = pd.read_csv('/content/Sleep_health_and_lifestyle_dataset.csv')
mega_gym_data = pd.read_csv('/content/megaGymDataset.csv')
fitness_data = pd.read_csv('/content/fitness_dataset.csv')

# Preprocess datasets
mega_gym_mapping = mega_gym_data.groupby('Level')['Title'].apply(list).to_dict()
fitness_data['Intensity'] = pd.cut(
    fitness_data['Calories per kg'],
    bins=[0, 1.0, 2.0, fitness_data['Calories per kg'].max()],
    labels=['Low', 'Medium', 'High']
)
fitness_mapping = fitness_data.groupby('Intensity')['Activity, Exercise or Sport (1 hour)'].apply(list).to_dict()

exercise_mapping = {
    "Low": fitness_mapping.get('Low', []) + mega_gym_mapping.get('Beginner', []),
    "Medium": fitness_mapping.get('Medium', []) + mega_gym_mapping.get('Intermediate', []),
    "High": fitness_mapping.get('High', []) + mega_gym_mapping.get('Advanced', [])
}

# Recommendation Function
def recommend_exercise(age, weight, sleep_duration, occupation, sleep_disorder):
    # Map occupation and sleep disorder to categories
    if sleep_disorder == 'Yes' and occupation == 'Sedentary':
        category = "Low"
    elif sleep_disorder == 'No' and occupation == 'Active':
        category = "Medium"
    else:
        category = "High"
    
    # Fetch exercises
    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(category, []), min(7, len(mega_gym_mapping.get(category, []))))
    return fitness_exercises + gym_exercises

# Streamlit App
st.title("Exercise Recommendation System")
st.header("Provide your details to get personalized exercise recommendations")

# User Inputs
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)
sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0)
occupation = st.selectbox("Occupation", ["Sedentary", "Active"])
sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"])

# Generate Recommendation
if st.button("Recommend Exercises"):
    recommended_exercises = recommend_exercise(age, weight, sleep_duration, occupation, sleep_disorder)
    st.success("Recommended Exercises:")
    st.write(", ".join(recommended_exercises))


