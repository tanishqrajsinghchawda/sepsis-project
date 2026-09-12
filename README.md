# 🏥 AI-Based Sepsis Early Warning System for ICU Patients

An end-to-end machine learning system that predicts sepsis risk in ICU patients using hourly vitals and lab data, with SHAP-based explanations for every prediction — built as an MCA minor project.

## Problem

Sepsis is a leading cause of ICU death, with mortality rates in India (25–36%) higher than the global average. Early detection significantly improves outcomes, but manual monitoring is slow and inconsistent under ICU workload. This project predicts sepsis risk in real time from patient vitals and explains why each prediction was made.

## Dataset

PhysioNet / Computing in Cardiology Challenge 2019 — 40,336 ICU patients, hourly vitals and labs, sepsis outcome labels. (Kaggle: https://www.kaggle.com/datasets/salikhussaini49/prediction-of-sepsis)

## Approach

1. Data Cleaning & Aggregation — collapsed 1.55M hourly rows into one row per patient (vitals as mean/min/max, labs as last known value with "was tested" flags, engineered Shock Index feature)
2. Model Training — compared Logistic Regression, Random Forest, and XGBoost; selected XGBoost (F1: 0.68) for the best precision/recall balance on this imbalanced dataset (7.27% sepsis rate)
3. Explainability — SHAP used to show which factors drove each individual prediction, not just a black-box score
4. Deployment — packaged as an interactive Streamlit app with prediction history stored in SQLite

## Tech Stack

Python, Pandas, NumPy, scikit-learn, XGBoost, SHAP, Streamlit, SQLite

## Project Structure

sepsis-project/
- data/ — raw and processed datasets (not tracked in git)
- notebooks/01_data_acquisition.ipynb — data loading, EDA, patient-level aggregation, cleaning & feature engineering (Phases 1-4)
- notebooks/05_model_training.ipynb — model training & comparison, SHAP explainability, model export, app development (Phases 5-8)
- figures/ — saved plots for the report
- app/ — Streamlit app, trained model, database
- docs/ — progress log, report

## Running the App

conda activate booksenv
streamlit run app/app.py

## Results

| Model | Precision (sepsis) | Recall (sepsis) | F1 |
|---|---|---|---|
| Logistic Regression | 0.21 | 0.75 | 0.33 |
| Random Forest | 0.85 | 0.44 | 0.58 |
| XGBoost (selected) | 0.68 | 0.68 | 0.68 |

## Author

Tanishq Raj Singh Chawda— MCA, Medicaps University, Indore