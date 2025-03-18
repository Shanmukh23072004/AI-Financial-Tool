
from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    plt.figure(figsize=(8,4))
    plt.plot([1,2,3,4], [10,20,30,40])  # Dummy plot
    plt.title(f'Stock Prediction for {ticker}')
    plt.savefig('static/images/stock.png')
    plt.close()
    return render_template('result.html', result=f'Stock prediction for {ticker}', image='images/stock.png')

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

@app.route('/credit', methods=['POST'])
def credit():
    score = int(request.form['score'])
    result = "Good Credit Score" if score >= 700 else "Needs Improvement"
    return render_template('result.html', result=f"Your Credit Score Analysis: {result}")

if __name__ == '__main__':
    app.run(debug=True)
