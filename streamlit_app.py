import streamlit as st
import pandas as pd
import numpy as np
import random
import altair as alt
import sqlite3
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Database setup
conn = sqlite3.connect('health_data.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    weight REAL,
    stress_level INTEGER,
    sleep_duration REAL,
    blood_pressure INTEGER
)
''')
conn.commit()

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

# Train a Random Forest Classifier
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
rf_clf = RandomForestClassifier(random_state=42, n_estimators=100)
rf_clf.fit(X_train, y_train)
accuracy = accuracy_score(y_test, rf_clf.predict(X_test))

# Fetch data from database
health_data = pd.read_sql_query("SELECT * FROM health_performance", conn)
if not health_data.empty:
    health_data['Date'] = pd.to_datetime(health_data['date'])

# Custom CSS for Modern UI
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
    body {
        font-family: 'Arial', sans-serif;
        background-color: #e1f5fe; /* Baby Blue Background */
        color: #333;
    }
    .header {
        background-color: #039be5; /* Blue Header */
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 20px;
    }
    .container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        font-size: 0.9rem;
        color: #666;
    }
    .footer span {
        color: #039be5;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">Personalized Fitness Plan</div>', unsafe_allow_html=True)

# Manage Health Data Section
st.markdown("## Manage Your Health Metrics")
if not health_data.empty:
    st.dataframe(health_data)

    # Select a record to edit or delete
    selected_id = st.selectbox("Select a record to edit or delete", health_data["id"])

    # Load the selected record
    selected_record = health_data[health_data["id"] == selected_id]
    if not selected_record.empty:
        selected_date = selected_record.iloc[0]["date"]
        selected_weight = selected_record.iloc[0]["weight"]
        selected_stress_level = selected_record.iloc[0]["stress_level"]
        selected_sleep_duration = selected_record.iloc[0]["sleep_duration"]
        selected_blood_pressure = selected_record.iloc[0]["blood_pressure"]

        # Edit or Delete Form
        st.markdown("### Edit Selected Record")
        with st.form("edit_health_data"):
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=selected_weight)
            stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, value=selected_stress_level)
            sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=selected_sleep_duration)
            blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=80, max_value=200, value=selected_blood_pressure)
            save_changes = st.form_submit_button("Save Changes")
            delete_record = st.form_submit_button("Delete Record")

        if save_changes:
            cursor.execute('''
                UPDATE health_performance
                SET weight = ?, stress_level = ?, sleep_duration = ?, blood_pressure = ?
                WHERE id = ?
            ''', (weight, stress_level, sleep_duration, blood_pressure, selected_id))
            conn.commit()
            st.success("Record updated successfully! Refresh the page to see changes.")
        
        if delete_record:
            cursor.execute('DELETE FROM health_performance WHERE id = ?', (selected_id,))
            conn.commit()
            st.success("Record deleted successfully! Refresh the page to see changes.")
else:
    st.info("No health data available. Add new metrics below.")

# Update Health Data Form
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("### Add New Health Metrics")
with st.form("add_health_data"):
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, value=5)
    sleep_duration = st.number_input("Sleep Duration (hours)", min_value=1.0, max_value=12.0, value=7.0)
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
    add_record = st.form_submit_button("Add Metrics")

if add_record:
    cursor.execute(
        '''
        INSERT INTO health_performance (date, weight, stress_level, sleep_duration, blood_pressure)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (datetime.now().strftime("%Y-%m-%d"), weight, stress_level, sleep_duration, blood_pressure)
    )
    conn.commit()
    st.success("New metrics added successfully! Refresh the page to see changes.")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p><strong>Empower your fitness journey!</strong> Designed with <span>♥</span> using Streamlit.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

conn.close()


























