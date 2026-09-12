import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Sepsis Early Warning System",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #f5f9fc;
    }
    .stApp {
        background-color: #f5f9fc;
    }
    h1 {
        color: #0b4f6c;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #0b4f6c;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #083a52;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 Sepsis Early Warning System")
st.caption("AI-assisted risk assessment for ICU patients")

model = joblib.load('app/model.joblib')
explainer = shap.TreeExplainer(model)

with st.sidebar:
    st.header("📋 Patient Details")

    st.subheader("Demographics")
    age = st.number_input("Age", min_value=0, max_value=120, value=50)
    gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male" if x == 0 else "Female")

    st.subheader("Vitals")
    hr_mean = st.number_input("Heart Rate - avg (bpm)", min_value=0.0, max_value=250.0, value=80.0)
    temp_max = st.number_input("Temperature - max (°C)", min_value=30.0, max_value=45.0, value=37.0)
    sbp_min = st.number_input("Systolic BP - min (mmHg)", min_value=0.0, max_value=300.0, value=110.0)
    resp_mean = st.number_input("Respiratory Rate - avg", min_value=0.0, max_value=100.0, value=18.0)
    iculos_max = st.number_input("Hours in ICU so far", min_value=0, max_value=500, value=24)

    st.subheader("Key Labs")
    wbc_last = st.number_input("WBC (white blood cells)", min_value=0.0, max_value=100.0, value=8.0)
    creatinine_last = st.number_input("Creatinine", min_value=0.0, max_value=20.0, value=1.0)

    predict_button = st.button("🔍 Check Sepsis Risk", use_container_width=True)

tab1, tab2 = st.tabs(["🔍 New Prediction", "📊 Patient History"])

with tab1:
    if predict_button:
        medians = pd.read_csv('app/feature_medians.csv', index_col=0).iloc[:, 0]

        input_data = pd.DataFrame([medians])

        input_data['Age'] = age
        input_data['Gender'] = gender
        input_data['HR_mean'] = hr_mean
        input_data['HR_min'] = hr_mean
        input_data['HR_max'] = hr_mean
        input_data['Temp_mean'] = temp_max
        input_data['Temp_min'] = temp_max
        input_data['Temp_max'] = temp_max
        input_data['SBP_mean'] = sbp_min
        input_data['SBP_min'] = sbp_min
        input_data['SBP_max'] = sbp_min
        input_data['Resp_mean'] = resp_mean
        input_data['Resp_min'] = resp_mean
        input_data['Resp_max'] = resp_mean
        input_data['WBC_last'] = wbc_last
        input_data['Creatinine_last'] = creatinine_last
        input_data['ICULOS_max'] = iculos_max

        input_data = input_data[model.feature_names_in_]

        risk_prob = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

        st.header("Prediction Result")

        if prediction == 1:
            st.error(f"⚠️ HIGH RISK — Sepsis probability: {risk_prob*100:.1f}%")
        else:
            st.success(f"✅ LOW RISK — Sepsis probability: {risk_prob*100:.1f}%")

        st.progress(float(risk_prob))

        st.subheader("Why this prediction?")

        shap_values = explainer.shap_values(input_data)

        shap.force_plot(explainer.expected_value, shap_values[0], input_data.iloc[0],
                         matplotlib=True, show=False)
        fig = plt.gcf()
        st.pyplot(fig)
        plt.close(fig)

        conn = sqlite3.connect('app/sepsis.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_predictions (timestamp, age, gender, hr_mean, temp_max, sbp_min, risk_score, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), age, gender, hr_mean, temp_max, sbp_min, float(risk_prob), int(prediction)))
        conn.commit()
        conn.close()

        st.caption("✓ Saved to patient history")
    else:
        st.info("👈 Enter patient details in the sidebar and click 'Check Sepsis Risk' to begin.")

with tab2:
    conn = sqlite3.connect('app/sepsis.db')
    history_df = pd.read_sql_query("SELECT * FROM patient_predictions ORDER BY id DESC", conn)
    conn.close()

    if len(history_df) == 0:
        st.info("No patients checked yet. Predictions will appear here once you use the form.")
    else:
        st.subheader(f"Total patients checked: {len(history_df)}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Risk Score Distribution")
            fig1, ax1 = plt.subplots()
            ax1.hist(history_df['risk_score'], bins=10, color='#0b4f6c')
            ax1.set_xlabel("Risk Score")
            ax1.set_ylabel("Number of Patients")
            st.pyplot(fig1)
            plt.close(fig1)

        with col2:
            st.write("High Risk vs Low Risk Count")
            counts = history_df['prediction'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.bar(['Low Risk', 'High Risk'],
                    [counts.get(0, 0), counts.get(1, 0)],
                    color=['#4caf50', '#e53935'])
            st.pyplot(fig2)
            plt.close(fig2)

        st.subheader("Recent Patients")
        st.dataframe(history_df, use_container_width=True)