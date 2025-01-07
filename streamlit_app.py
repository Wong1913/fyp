import streamlit as st
import pandas as pd
import numpy as np
import random
import altair as alt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Simulated progress data (to be replaced with a database in a real application)
progress_data = pd.DataFrame({
    'Date': pd.date_range(start="2025-01-01", periods=10, freq='D'),
    'Intensity': np.random.choice(['Low', 'Medium', 'High'], size=10),
    'Calories Burned': np.random.randint(100, 500, size=10),
    'Duration (mins)': np.random.randint(30, 120, size=10)
})

# Load datasets
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

# Train a Decision Tree Classifier (placeholder logic)
df = pd.DataFrame({
    'Age': [25, 55, 35, 60, 20],
    'Weight': [70, 90, 80, 85, 60],
    'Occupation': [0, 1, 1, 1, 0],  # 0: Active, 1: Sedentary
    'Sleep_Disorder': [0, 1, 0, 1, 0],  # 0: No, 1: Yes
    'Sleep_Duration': [7, 5, 6, 5, 8],
    'Stress_Level': [3, 8, 5, 7, 2],
    'Blood_Pressure': [120, 145, 130, 150, 110],
    'Category': ['High', 'Low', 'Medium', 'Low', 'High']
})
X = df[['Age', 'Weight', 'Occupation', 'Sleep_Disorder', 'Sleep_Duration', 'Stress_Level', 'Blood_Pressure']]
y = df['Category']
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
accuracy = accuracy_score(y_test, clf.predict(X_test))

# UI with Light/Dark Mode
theme = st.sidebar.radio("Select Theme", ['Light', 'Dark'])
if theme == 'Dark':
    st.markdown(
        """
        <style>
        body { background-color: #121212; color: white; }
        .container { background-color: #1e1e1e; color: white; }
        .recommendation { background-color: #242424; }
        .footer { color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #e3f2fd; color: black; }
        .container { background-color: white; color: black; }
        .recommendation { background-color: #e3f2fd; }
        .footer { color: black; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Header
st.markdown('<div class="header">Exercise Recommendation System</div>', unsafe_allow_html=True)

# Progress Tracking Section
st.markdown("## Your Progress Over Time")
chart = alt.Chart(progress_data).mark_line(point=True).encode(
    x='Date:T',
    y='Calories Burned:Q',
    color='Intensity:N',
    tooltip=['Date:T', 'Calories Burned:Q', 'Duration (mins):Q', 'Intensity:N']
).interactive()
st.altair_chart(chart, use_container_width=True)

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
    # Predict Category
    user_data = scaler.transform([[
        age, weight, 
        0 if occupation == "Active" else 1,
        0 if sleep_disorder == "No" else 1,
        sleep_duration, stress_level, blood_pressure
    ]])
    predicted_category = clf.predict(user_data)[0]

    # Fetch Recommendations
    fitness_exercises = exercise_mapping.get(predicted_category, {}).get("fitness", [])
    gym_exercises = exercise_mapping.get(predicted_category, {}).get("gym", [])
    recommendations = random.sample(fitness_exercises, min(2, len(fitness_exercises))) + \
                      random.sample(gym_exercises, min(7, len(gym_exercises)))

    # Display Recommendations
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
        <p><strong>Track your fitness journey!</strong> Created with <span>♥</span> using Streamlit.</p>
    </div>
    """, 
    unsafe_allow_html=True
)


















