import yfinance as yf
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import os
import pickle

symbols = ["SBIN","RELIANCE","ADANIGREEN","ICICIPRULI","ONGC"]

def train_ticker(ticker):

    df = yf.download(f"{ticker}.NS")
    df = df.reset_index()
    print(df.tail())

    df[['ds','y']] = df[['Date','Close']]      
    train_data = df.sample(frac=0.8, random_state=0)
    model = Prophet(daily_seasonality=True)
    model.fit(train_data)
    model_folder = "models"
    os.makedirs(model_folder,exist_ok=True)
    model_path = os.path.join(model_folder,f"{ticker}.pkl")
    with open(model_path,"wb") as f:
        pickle.dump(model,f)


 

   
for symbol in symbols:
    train_ticker(symbol)
