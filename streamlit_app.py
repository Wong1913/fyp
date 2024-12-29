import streamlit as st
import pandas as pd
import random

# Load necessary datasets
@st.cache
def load_data():
    sleep_health_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/Sleep_health_and_lifestyle_dataset.csv')
    mega_gym_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/megaGymDataset.csv')
    fitness_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/fitness_dataset.csv')
    return sleep_health_data, mega_gym_data, fitness_data

sleep_health_data, mega_gym_data, fitness_data = load_data()

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
category_mapping = {"Low": "Beginner", "Medium": "Intermediate", "High": "Advanced"}

# Recommendation Function
def recommend_exercise(category):
    gym_category = category_mapping.get(category, "Beginner")
    fitness_exercises = random.sample(fitness_mapping.get(category, []), min(2, len(fitness_mapping.get(category, []))))
    gym_exercises = random.sample(mega_gym_mapping.get(gym_category, []), min(7, len(mega_gym_mapping.get(gym_category, []))))
    return fitness_exercises, gym_exercises

# Streamlit App
st.set_page_config(page_title="Exercise Recommendation System", page_icon="🏋️", layout="centered")

st.title("🏋️ Exercise Recommendation System")
st.write("**Get personalized exercise recommendations tailored to your fitness level and preferences.**")

# Sidebar for User Inputs
st.sidebar.header("Provide Your Details")
age = st.sidebar.slider("Age", min_value=1, max_value=120, value=30)
weight = st.sidebar.slider("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)
sleep_duration = st.sidebar.slider("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0)
occupation = st.sidebar.selectbox("Occupation", ["Sedentary", "Active"])
sleep_disorder = st.sidebar.selectbox("Do you have a sleep disorder?", ["Yes", "No"])

# Map inputs to fitness category
if sleep_disorder == "Yes" and occupation == "Sedentary":
    category = "Low"
elif sleep_disorder == "No" and occupation == "Active":
    category = "Medium"
else:
    category = "High"

# Generate Recommendation
if st.button("🔍 Get Recommendations"):
    fitness_exercises, gym_exercises = recommend_exercise(category)
    
    st.success("🎯 Your Recommended Exercises:")
    st.write("### 🏃‍♂️ Fitness Activities:")
    for exercise in fitness_exercises:
        st.write(f"- {exercise}")
    st.write("### 🏋️ Gym Activities:")
    for exercise in gym_exercises:
        st.write(f"- {exercise}")
    
    st.balloons()

# Footer
st.markdown(
    """
    ---
    **Made with ❤️ using [Streamlit](https://streamlit.io/)**  
    Developed by Your Name
    """
)









