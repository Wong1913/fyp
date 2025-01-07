import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load datasets
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
    "Low": {
        "fitness": fitness_mapping.get('Low', []),
        "gym": mega_gym_mapping.get('Beginner', [])
    },
    "Medium": {
        "fitness": fitness_mapping.get('Medium', []),
        "gym": mega_gym_mapping.get('Intermediate', [])
    },
    "High": {
        "fitness": fitness_mapping.get('High', []),
        "gym": mega_gym_mapping.get('Expert', [])
    }
}

# Prepare training data
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

# Map categorical variables
occupation_mapping = {'Active': 0, 'Sedentary': 1}
sleep_disorder_mapping = {'No': 0, 'Yes': 1}

df['Occupation'] = df['Occupation'].map(occupation_mapping)
df['Sleep_Disorder'] = df['Sleep_Disorder'].map(sleep_disorder_mapping)

# Split data
X = df[['Age', 'Weight', 'Occupation', 'Sleep_Disorder', 'Sleep_Duration', 'Stress_Level', 'Blood_Pressure']]
y = df['Category']

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Calculate model accuracy
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f7f9fc;
    }
    .header {
        background: linear-gradient(to right, #4caf50, #81c784);
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .subheader {
        text-align: center;
        color: #4caf50;
        font-size: 1.2rem;
        margin-top: -10px;
    }
    .container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .recommendation {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        font-size: 0.9rem;
        color: #757575;
    }
    .footer span {
        color: #4caf50;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">Advanced Exercise Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Personalized recommendations based on your lifestyle</div>', unsafe_allow_html=True)

# User Input Form
st.markdown('<div class="container">', unsafe_allow_html=True)
with st.form("user_details_form"):
    st.markdown("### Your Details")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)
    occupation = st.selectbox("Occupation", ["Active", "Sedentary"])
    sleep_disorder = st.selectbox("Do you have a sleep disorder?", ["Yes", "No"])
    sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0)
    stress_level = st.slider("Stress Level (2-10)", min_value=2, max_value=10, value=5)
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
    submit_button = st.form_submit_button("Generate Recommendations")
st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    # Validate inputs
    if age <= 0 or weight <= 0 or blood_pressure <= 0:
        st.error("Please provide valid inputs.")
    else:
        # Scale and Predict
        user_data = scaler.transform([[
            age, weight, 
            occupation_mapping.get(occupation, 1),
            sleep_disorder_mapping.get(sleep_disorder, 0),
            sleep_duration, stress_level, blood_pressure
        ]])
        predicted_category = clf.predict(user_data)[0]

        # Fetch recommendations
        fitness_exercises = exercise_mapping.get(predicted_category, {}).get("fitness", [])
        gym_exercises = exercise_mapping.get(predicted_category, {}).get("gym", [])
        selected_fitness_exercises = random.sample(fitness_exercises, min(2, len(fitness_exercises)))
        selected_gym_exercises = random.sample(gym_exercises, min(7, len(gym_exercises)))
        recommendations = selected_fitness_exercises + selected_gym_exercises

        # Display recommendations
        st.markdown('<div class="recommendation">', unsafe_allow_html=True)
        st.markdown(f"### Recommended Exercises ({predicted_category} Intensity)")
        if recommendations:
            for i, exercise in enumerate(recommendations, start=1):
                st.markdown(f"{i}. {exercise}")
        else:
            st.warning("No exercises available for the predicted category.")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p><strong>Stay healthy, stay active!</strong> Created with <span>♥</span> using Streamlit for your wellness journey.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
















