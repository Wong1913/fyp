import streamlit as st
import pandas as pd
import random

# Load datasets
@st.cache
def load_data():
    fitness_data = pd.read_csv('fitness_dataset.csv')
    mega_gym_data = pd.read_csv('megaGymDataset.csv')
    return fitness_data, mega_gym_data

fitness_data, mega_gym_data = load_data()

# Data processing
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

# Recommendation function
def recommend_exercise(category):
    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(category, []), min(7, len(mega_gym_mapping.get(category, []))))
    return fitness_exercises + gym_exercises

# Streamlit UI
st.title("Exercise Recommendation System")
st.header("Get personalized exercise recommendations!")

category = st.selectbox("Choose your fitness category:", ["Low", "Medium", "High"])

if st.button("Get Recommendations"):
    exercises = recommend_exercise(category)
    st.write("Recommended Exercises:")
    st.write(", ".join(exercises))


