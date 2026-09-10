from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Create FastAPI application
app = FastAPI()

# Load trained model
model = joblib.load("churn_model.pkl")


# Customer input
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float
    PaperlessBilling: int
    SeniorCitizen: int
    PhoneService: int
    Dependents: int
    TotalCharges: float
    Partner: int


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is Running"
    }


@app.post("/predict")
def predict(customer: Customer):

    # Convert input into DataFrame
    data = pd.DataFrame([{
        "tenure": customer.tenure,
        "MonthlyCharges": customer.MonthlyCharges,
        "PaperlessBilling": customer.PaperlessBilling,
        "SeniorCitizen": customer.SeniorCitizen,
        "PhoneService": customer.PhoneService,
        "Dependents": customer.Dependents,
        "TotalCharges": customer.TotalCharges,
        "Partner": customer.Partner
    }])

    # Keep the same order as training
    features = [
        "tenure",
        "MonthlyCharges",
        "PaperlessBilling",
        "SeniorCitizen",
        "PhoneService",
        "Dependents",
        "TotalCharges",
        "Partner"
    ]

    data = data[features]

    # Prediction
    prediction = model.predict(data)[0]

    # Probability
    probability = model.predict_proba(data)[0]

    if prediction == 1:
        result = "Customer will CHURN"
    else:
        result = "Customer will NOT CHURN"

    return {
        "prediction": int(prediction),
        "result": result,
        "no_churn_probability": float(probability[0]),
        "churn_probability": float(probability[1])
    }