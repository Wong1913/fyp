import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Load necessary datasets
sleep_health_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/Sleep_health_and_lifestyle_dataset.csv')
mega_gym_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/megaGymDataset.csv')
fitness_data = pd.read_csv('https://raw.githubusercontent.com/Wong1913/fyp/refs/heads/master/fitness_dataset.csv')

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
    "High": fitness_mapping.get('High', []) + mega_gym_mapping.get('Expert', [])
}

# Prepare training data for decision tree
data = {
    'Age': [25, 55, 35, 60, 20],
    'Weight': [70, 90, 80, 85, 60],
    'Occupation': ['Active', 'Sedentary', 'Sedentary', 'Sedentary', 'Active'],
    'Sleep_Disorder': ['No', 'Yes', 'No', 'Yes', 'No'],
    'Sleep_Duration': [7, 5, 6, 5, 8],
    'Stress_Level': [3, 8, 5, 7, 2],
    'Blood_Pressure': [120, 145, 130, 150, 110],
    'Category': ['High', 'Low', 'Medium', 'Low', 'High']
}

df = pd.DataFrame(data)

# Manually map categorical variables
occupation_mapping = {'Active': 0, 'Sedentary': 1}
sleep_disorder_mapping = {'No': 0, 'Yes': 1}

df['Occupation'] = df['Occupation'].map(occupation_mapping)
df['Sleep_Disorder'] = df['Sleep_Disorder'].map(sleep_disorder_mapping)

# Split data into features and labels
X = df[['Age', 'Weight', 'Occupation', 'Sleep_Disorder', 'Sleep_Duration', 'Stress_Level', 'Blood_Pressure']]
y = df['Category']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Streamlit App
st.set_page_config(page_title="Exercise Recommendation System", page_icon="🏋️", layout="wide")
st.markdown('<h1 style="text-align: center; color: #01579b;">Exercise Recommendation System</h1>', unsafe_allow_html=True)

st.markdown('<h3>Enter your details for personalized exercise recommendations:</h3>', unsafe_allow_html=True)

# User Inputs
with st.form("user_details_form"):
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)
    occupation = st.selectbox("Occupation", ["Active", "Sedentary"])
    sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"])
    sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0)
    stress_level = st.slider("Stress Level (2-10)", min_value=2, max_value=10, value=5)
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
    submit_button = st.form_submit_button("Generate Recommendations")

if submit_button:
    # Map user inputs using the same mappings
    user_occupation = occupation_mapping.get(occupation, 1)  # Default to 'Sedentary' if unknown
    user_sleep_disorder = sleep_disorder_mapping.get(sleep_disorder, 0)  # Default to 'No' if unknown

    # Create user input DataFrame
    user_data = pd.DataFrame({
        'Age': [age],
        'Weight': [weight],
        'Occupation': [user_occupation],
        'Sleep_Disorder': [user_sleep_disorder],
        'Sleep_Duration': [sleep_duration],
        'Stress_Level': [stress_level],
        'Blood_Pressure': [blood_pressure]
    })

    # Predict exercise category
    predicted_category = clf.predict(user_data)[0]

    # Fetch recommendations
    recommended_exercises = exercise_mapping.get(predicted_category, [])
    st.markdown(f"<h3>Recommended Exercises ({predicted_category} Intensity):</h3>", unsafe_allow_html=True)
    
    if recommended_exercises:
        # Limit the number of exercises displayed
        num_exercises_to_show = min(10, len(recommended_exercises))
        exercises_to_show = random.sample(recommended_exercises, num_exercises_to_show)
        for i, exercise in enumerate(exercises_to_show, start=1):
            st.markdown(f"{i}. {exercise}")
    else:
        st.warning("No exercises available for the predicted category. Please adjust your inputs.")

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p><strong>Stay healthy, stay active!</strong> Created with <span style="color: red;">♥</span> using Streamlit for your wellness journey.</p>
    </div>
    """,
    unsafe_allow_html=True
)













