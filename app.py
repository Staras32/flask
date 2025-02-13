from flask import Flask, jsonify
import random  # Naudojame atsitiktinius signalus kaip pavyzdį

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the XAUsD Signal Generator!"

@app.route('/get_signal', methods=['GET'])
def get_signal():
    # Čia galite sukurti logiką, kuri apskaičiuos signalą pagal jūsų strategiją
    signals = ['Buy Signal', 'Sell Signal', 'No Signal']
    # Atsitiktinis pasirinkimas signalų sąraše
    signal = random.choice(signals)
    return jsonify({"signal": signal})

if __name__ == '__main__':
    app.run(debug=True)
