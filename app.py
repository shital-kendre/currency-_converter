from flask import Flask, jsonify, request, render_template
import config

app = Flask(__name__)



exchange_rates = {
    "USD": 1.0,
    "EUR": 0.93,
    "GBP": 0.81,
    "JPY": 130.0,
    "INR": 82.0
}

@app.route('/')
def home():
    return render_template('index.html', image_path = config.IMAGE_PATH)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.form  
    print("Data:", data)

    if not data:
        return jsonify({"Response": "Failed", "Error": "Provide input"}), 400

    # Retrieve input values from JSON
    input_currency = data.get('input_currency')
    target_currency = data.get('target_currency')
    
    # Validate and convert amount
    try:
        amount = float(data.get('amount'))
    except (ValueError, TypeError):
        return jsonify({"Response": "Failed", "Error": "Invalid amount provided"}), 400

    # Check if currencies are supported
    if input_currency not in exchange_rates or target_currency not in exchange_rates:
        return jsonify({"Response": "Failed", "Error": "Entered unsupported code"}), 400

    # Conversion: convert the source amount to USD, then to the target currency
    amount_in_usd = amount / exchange_rates[input_currency]
    converted_amount = amount_in_usd * exchange_rates[target_currency]

    print("Conversion successful")
    return jsonify({
        "Response": "Successful",
        "input_currency": input_currency,
        "target_currency": target_currency,
        "original_amount": amount,
        "converted_amount": round(converted_amount, 2)
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
