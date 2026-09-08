import streamlit as st
import pandas as pd
import joblib

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