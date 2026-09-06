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