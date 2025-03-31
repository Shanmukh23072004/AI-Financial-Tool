from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fd', methods=['POST'])
def fd():
    principal = float(request.form['principal'])
    rate = float(request.form['rate'])
    time = float(request.form['time'])
    maturity = principal * ((1 + rate/100) ** time)
    return render_template('result.html', result=f"FD Maturity Amount: ₹{maturity:.2f}")

@app.route('/emi', methods=['POST'])
def emi():
    loan = float(request.form['loan'])
    rate = float(request.form['rate']) / (12 * 100)
    time = int(request.form['time'])
    emi = (loan * rate * ((1 + rate) ** time)) / (((1 + rate) ** time) - 1)
    return render_template('result.html', result=f"Monthly EMI: ₹{emi:.2f}")

@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker'].upper()
    stock = yf.Ticker(ticker)
    df = stock.history(period='6mo')
    
    if df.empty:
        return render_template('result.html', result=f"Invalid stock ticker: {ticker}")
    
    df['Date'] = df.index
    df["Days"] = (df["Date"] - df["Date"].min()).dt.days
    
    X = df[['Days']]
    y = df['Close']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    future_dates = [df['Date'].max() + timedelta(days=i) for i in range(1, 8)]
    future_days = [(date - df['Date'].min()).days for date in future_dates]
    future_prices = model.predict(np.array(future_days).reshape(-1, 1))
    
    plt.figure(figsize=(12, 5))
    plt.scatter(X, y, color='blue', label='Historical Prices')
    plt.plot(X, model.predict(X), color='red', label='Regression Line')
    plt.scatter(future_days, future_prices, color='green', marker='X', label='Predicted Prices')
    
    plt.xlabel('Days Since Start')
    plt.ylabel('Stock Price (₹)')
    plt.title(f'Stock Price Prediction for {ticker}')
    plt.legend()
    plt.grid(True)
    
    image_path = 'static/images/stock_prediction.png'
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    plt.savefig(image_path)
    plt.close()
    
    predictions = {date.strftime('%Y-%m-%d'): round(price, 2) for date, price in zip(future_dates, future_prices)}
    return render_template('result.html', result=f'Stock Price Prediction for {ticker}', image='images/stock_prediction.png', predictions=predictions)

@app.route('/credit', methods=['POST'])
def credit():
    score = int(request.form['score'])
    result = "Good Credit Score" if score >= 700 else "Needs Improvement"
    return render_template('result.html', result=f"Your Credit Score Analysis: {result}")

@app.route('/market-trends', methods=['GET', 'POST'])
def market_trends():
    stock_data = None
    stock_image = None
    
    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="1mo")

            if df.empty:
                return render_template('market_trends.html', error="Invalid stock ticker or no data available.")

            # Reset index and convert Date to string format
            df.reset_index(inplace=True)
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')  # Convert datetime to string

            plt.figure(figsize=(10, 5))
            plt.plot(df['Date'], df['Close'], label=f"{ticker} Closing Price", color="blue")
            plt.xlabel("Date")
            plt.ylabel("Price (₹)")
            plt.title(f"{ticker} Stock Price Trend")
            plt.legend()
            plt.grid()

            img_path = f"static/{ticker}_trend.png"
            plt.savefig(img_path)
            plt.close()

            stock_image = img_path
            stock_data = df.tail(5).to_dict(orient='records')  # Convert DataFrame to list of dictionaries

        except Exception as e:
            return render_template('market_trends.html', error=f"Error fetching data: {str(e)}")

    return render_template('market_trends.html', stock_data=stock_data, stock_image=stock_image)

if __name__ == '__main__':
    app.run(debug=True)