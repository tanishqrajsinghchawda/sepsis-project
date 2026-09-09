## 02-09-2026
Loaded dataset (1,552,210 rows, 40,336 patients), confirmed class imbalance (98.2% vs 1.8% sepsis). Environment, Git, and GitHub fully set up. Ready for Phase 2 (EDA) next.

## 03-09-2026
Completed missing-data analysis (labs 90-99% missing, vitals 9-31% missing - expected pattern). Found 7.27% of patients (2932/40336) developed sepsis at some point, vs 1.8% row-level rate. Confirmed vitals show clinically expected differences (HR, Temp, Resp higher; MAP lower in sepsis rows), visualized with boxplots. Ready for Phase 3 (Patient-Level Aggregation) next.

## 04-09-2026
Completed Phase 3 (Patient-Level Aggregation). Aggregated 1.55M hourly rows into 40,336 patient-level rows (57 columns): vitals as mean/min/max, labs as last known value, static features as first value, SepsisLabel as max. Validated target distribution matches patient-level sepsis rate (2932/40336, 7.27%). Saved to data/processed/patient_level_data.csv.

## 05-09-2026
Completed Phase 4 (Cleaning & Feature Engineering). Dropped 4 columns over 90% missing. Added 25 "was this test done" flag columns before imputing labs with median values. Filled Unit1/Unit2 missing values with -1 (unknown category). Zero missing values remain across the dataset. Added Shock_Index_mean (HR/SBP) as an engineered feature - confirmed higher in sepsis patients (0.75 vs 0.69). Saved final dataset to data/processed/patient_level_final.csv (40336 rows, 79 columns).

## 05-09-2026 (continued)
Completed Phase 5 (Model Training & Comparison). Trained and evaluated three models on the 80/20 stratified train-test split: Logistic Regression (Recall 0.75, Precision 0.21, F1 0.33), Random Forest (Recall 0.44, Precision 0.85, F1 0.58), XGBoost (Recall 0.68, Precision 0.68, F1 0.68). Selected XGBoost as the final model for the most balanced precision/recall tradeoff and highest F1-score. Ready for Phase 6 (SHAP Explainability) next session.
## 06-09-2026 
Completed Phase 6 (Explainability). Generated SHAP global summary plot for XGBoost - top predictors are ICULOS_max (ICU stay length), Temp_max, HospAdmTime, WBC_last, and several lab "was tested" flags, confirming the missingness-as-signal decision from Phase 4 was useful. Generated a per-patient SHAP force plot showing individual reasoning (e.g. fever pushing risk up, normal creatinine/blood pressure pushing risk down) - this becomes the "reason" shown in the app. Ready for Phase 7 (Model Export & SQL Setup) next.
 ## 07-09-2026 
(continued) Completed Phase 7 (Model Export & SQL Setup). Saved trained XGBoost model to app/model.joblib using joblib. Created app/sepsis.db with a patient_predictions table (id, timestamp, age, gender, hr_mean, temp_max, sbp_min, risk_score, prediction). Verified the table structure and tested a full insert-then-read cycle before clearing the test row. Ready for Phase 8 (Unified Streamlit App) next session. 
 ## 08-09-2026 
 Started Phase 8 (Streamlit App). Built clinical-themed UI (light blue background, custom button styling, hospital emoji branding) with a sidebar input form (Demographics, Vitals, Key Labs) and a main-area prediction result. Fixed a bug where unfilled fields defaulted to 0, which let ICULOS_max (the strongest predictor) override extreme vitals - fixed by filling unspecified fields with training-data medians instead of zero, and adding ICU hours as a real input field. Verified with test cases: normal vitals gave 0.3% risk, extreme vitals gave 94.8% risk. Remaining for Phase 8: SHAP reason display, database logging, and history charts.