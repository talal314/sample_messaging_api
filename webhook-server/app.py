from flask import Flask, request, jsonify
import hmac
from sample_messaging.api.webhooks import generateSignature

app = Flask(__name__)


@app.route('/webhooks', methods=['POST'])
def handle_webhook():
    secret = 'mySecret'

    recieved_signature = request.headers.get('Authorization')

    payload = request.get_data(as_text=True)

    expected_signature = generateSignature(payload, secret)

    if hmac.compare_digest(recieved_signature, expected_signature):
        print("Valid signature...")
        data = request.json
        return jsonify({"message": "Webhooks received!", "data": data}), 200
    else:
        print("Invalid signature...")
        return jsonify({"error": "Invalid signature"}), 403
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3010)
