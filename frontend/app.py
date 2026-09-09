import streamlit as st
import requests

st.title("Customer Churn Prediction")

st.write("Enter customer details below:")

tenure = st.number_input("Tenure", min_value=0, value=24)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=65.5
)

paperless_billing = st.selectbox(
    "Paperless Billing",
    ["No", "Yes"]
)

senior_citizen = st.selectbox(
    "Senior Citizen",
    ["No", "Yes"]
)

phone_service = st.selectbox(
    "Phone Service",
    ["No", "Yes"]
)

dependents = st.selectbox(
    "Dependents",
    ["No", "Yes"]
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=1572.0
)

partner = st.selectbox(
    "Partner",
    ["No", "Yes"]
)


if st.button("Predict Churn"):

    data = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "PaperlessBilling": 1 if paperless_billing == "Yes" else 0,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
        "PhoneService": 1 if phone_service == "Yes" else 0,
        "Dependents": 1 if dependents == "Yes" else 0,
        "TotalCharges": total_charges,
        "Partner": 1 if partner == "Yes" else 0
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data
        )

        if response.status_code == 200:

          result = response.json()

          prediction = int(result["prediction"])

          if prediction == 1:
            st.error("⚠️ Yes, the customer will churn.")
          else:
            st.success("✅ No, the customer will not churn.")
        

        else:
            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to FastAPI. "
            "Make sure FastAPI is running."
        )