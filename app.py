from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import talib

# Įkrauti aplinkos kintamuosius iš .env failo
load_dotenv()

app = Flask(__name__)

# Gauti API raktą iš aplinkos kintamųjų
API_KEY = os.getenv('IAIC9NF8ZU7BP6UQ')

def get_alpha_vantage_data(symbol, interval, api_key):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.astype(float)
        return df
    else:
        return None

@app.route('/get_signal', methods=['GET'])
def get_signal():
    symbol = 'XAUUSD'
    interval = 'Daily'

    df = get_alpha_vantage_data(symbol, interval, API_KEY)

    if df is not None:
        rsi = talib.RSI(df['Close'], timeperiod=14)
        sma = talib.SMA(df['Close'], timeperiod=50)

        signal = None
        if rsi[-1] < 30:
            signal = "Buy Signal"
        elif rsi[-1] > 70:
            signal = "Sell Signal"
        elif df['Close'][-1] > sma[-1]:
            signal = "Buy Signal"
        elif df['Close'][-1] < sma[-1]:
            signal = "Sell Signal"
        else:
            signal = "Hold Signal"

        return jsonify({
            "signal": signal,
            "RSI": rsi[-1],
            "SMA": sma[-1],
            "last_price": df['Close'][-1]
        })
    else:
        return jsonify({"error": "Nepavyko gauti duomenų iš Alpha Vantage"})

if __name__ == '__main__':
    app.run(debug=True)
