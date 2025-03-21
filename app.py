<<<<<<< HEAD
=======

>>>>>>> 04e1373be1d8673aff572c25906189c1b1edd69c
from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
<<<<<<< HEAD
import yfinance as yf
import os
=======
>>>>>>> 04e1373be1d8673aff572c25906189c1b1edd69c

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

<<<<<<< HEAD
=======
@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    plt.figure(figsize=(8,4))
    plt.plot([1,2,3,4], [10,20,30,40])  # Dummy plot
    plt.title(f'Stock Prediction for {ticker}')
    plt.savefig('static/images/stock.png')
    plt.close()
    return render_template('result.html', result=f'Stock prediction for {ticker}', image='images/stock.png')

>>>>>>> 04e1373be1d8673aff572c25906189c1b1edd69c
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

<<<<<<< HEAD
@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    stock_data = yf.download(ticker, period='1mo', interval='1d')
    if stock_data.empty:
        return render_template('result.html', result=f"Invalid stock ticker: {ticker}")

    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], marker='o')
    plt.title(f'Stock Price for {ticker.upper()}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    image_path = 'static/images/stock.png'
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    plt.savefig(image_path)
    plt.close()

    return render_template('result.html', result=f'Stock Price Chart for {ticker.upper()}', image='images/stock.png')

=======
>>>>>>> 04e1373be1d8673aff572c25906189c1b1edd69c
@app.route('/credit', methods=['POST'])
def credit():
    score = int(request.form['score'])
    result = "Good Credit Score" if score >= 700 else "Needs Improvement"
    return render_template('result.html', result=f"Your Credit Score Analysis: {result}")

if __name__ == '__main__':
    app.run(debug=True)
<<<<<<< HEAD

=======
>>>>>>> 04e1373be1d8673aff572c25906189c1b1edd69c
