from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to saved models directory
MODEL_DIR = "models"

@app.get("/")
def read_root():
    return {"message": "Stock Prediction API"}

@app.get("/predict")
def predict_stock(ticker: str, days: int , start_date: str = None):
    model_path = os.path.join(MODEL_DIR, f"{ticker.lower()}.pkl")
    
    if not os.path.exists(model_path):
        return {"success": False, "error": f"Model for {ticker} not found."}
    
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        return {"success": False, "error": f"Error loading model: {str(e)}"}
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return {"success": False, "error": "Invalid start date format. Use YYYY-MM-DD."}

    
    future_dates = model.make_future_dataframe(periods=days)
    forecast = model.predict(future_dates)
    
    forecast = forecast[forecast["ds"] >= pd.Timestamp(start_date)]
    result = forecast.head(days)[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")
    
    return {"success": True, "forecast": result}
