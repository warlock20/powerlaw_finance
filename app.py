from flask import Flask, render_template, request, jsonify
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    ticker = request.form['ticker'].upper()
    end_date = datetime(2025, 1, 20)
    start_date = end_date - timedelta(days=3650)

    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)

    data['Open-Close Difference'] = data['Close'] - data['Open']

    plt.figure(figsize=(12, 6))
    plt.hist(data['Open-Close Difference'], bins=50, edgecolor='black')
    plt.title(f'Histogram of {ticker} Daily Open-Close Differences (Last 10 Years)')
    plt.xlabel('Difference (Close - Open)')
    plt.ylabel('Frequency')
    plt.axvline(x=0, color='red', linestyle='--', linewidth=1)

    mean_diff = data['Open-Close Difference'].mean()
    median_diff = data['Open-Close Difference'].median()
    plt.text(0.05, 0.95, f'Mean: {mean_diff:.2f}\nMedian: {median_diff:.2f}', 
             transform=plt.gca().transAxes, verticalalignment='top')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()

    return jsonify({
        'image': img_str,
        'ticker': ticker
    })

if __name__ == '__main__':
    app.run(debug=True)
