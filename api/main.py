from pathlib import Path
import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


# =========================
# Load Model
# =========================

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        Path(__file__).resolve().parent.parent / "attendance_model.joblib"
    )
)
print("Loading model from:", MODEL_PATH)

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")


# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="Smart Attendance AI API",
    description="API for attendance risk prediction",
    version="1.0.0"
)


# =========================
# Input Schema
# =========================

class AttendanceInput(BaseModel):
    previous_attendance: float
    recent_3week_attendance: float
    previous_late_rate: float
    previous_absence_rate: float
    previous_course_load: float
    attendance_trend: float


# =========================
# Root Endpoint
# =========================

@app.get("/")
def root():
    return {
        "message": "Smart Attendance AI API is running"
    }


# =========================
# Health Check
# =========================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True
    }


# =========================
# Prediction
# =========================

@app.post("/predict")
def predict(data: AttendanceInput):

    input_data = pd.DataFrame([{
        "previous_attendance": data.previous_attendance,
        "recent_3week_attendance": data.recent_3week_attendance,
        "previous_late_rate": data.previous_late_rate,
        "previous_absence_rate": data.previous_absence_rate,
        "previous_course_load": data.previous_course_load,
        "attendance_trend": data.attendance_trend
    }])

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    if probability >= 0.70:
        risk_level = "HIGH"
    elif probability >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_probability": round(float(probability), 4),
        "prediction": int(prediction),
        "risk_level": risk_level
    }