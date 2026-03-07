import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "credit_model.pkl")

model = joblib.load(MODEL_PATH)

def predict(data):

    features = [[
        data["income"],
        data["age"],
        data["employment_years"],
        data["loan_amount"],
        data["loan_term"],
        data["credit_history_length"],
        data["num_credit_lines"],
        data["num_delinquencies"],
        data["debt_to_income_ratio"],
        data["savings_balance"]
    ]]

    prob = model.predict_proba(features)[0][1]
    approved = prob > 0.5

    if prob > 0.8:
        risk = "Low"
        recommendation = "Loan likely safe to approve."
    elif prob > 0.5:
        risk = "Medium"
        recommendation = "Review application before approval."
    else:
        risk = "High"
        recommendation = "High risk applicant."

    return {
        "approval_score": float(prob),
        "approved": bool(approved),
        "risk_level": risk,
        "recommendation": recommendation
    }