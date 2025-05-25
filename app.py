from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory store
tokens = {}  # Example: {'PAID-1234': {'uses': 3}}

# ✅ Validate token for Colab
@app.route('/validate-token', methods=['POST'])
def validate_token():
    data = request.get_json()
    token = data.get('token')
    
    if not token or token not in tokens:
        return jsonify({"valid": False}), 401
    
    if tokens[token]['uses'] <= 0:
        return jsonify({"valid": False, "remaining_uses": 0}), 403
    
    return jsonify({"valid": True, "remaining_uses": tokens[token]['uses']}), 200

# ✅ Simulate use of token (optional, not used by Colab)
@app.route('/use-token', methods=['POST'])
def use_token():
    data = request.get_json()
    token = data.get('token')
    
    if token in tokens and tokens[token]['uses'] > 0:
        tokens[token]['uses'] -= 1
        return jsonify({"success": True, "remaining_uses": tokens[token]['uses']})
    
    return jsonify({"success": False}), 400

# ✅ Generate a test token manually (for dev/test only)
@app.route('/generate-token', methods=['GET'])
def generate_token():
    token = f"PAID-{uuid.uuid4().hex[:6].upper()}"
    tokens[token] = {'uses': 3}
    return jsonify({"token": token, "uses": 3})

# ✅ Handle PayHere webhook
@app.route('/webhook/payhere', methods=['POST'])
def payhere_webhook():
    data = request.form
    status = data.get('status')
    customer_email = data.get('customer_email')

    if status == 'Charged':
        token = f"PAID-{uuid.uuid4().hex[:6].upper()}"
        tokens[token] = {'uses': 3}
        print(f"[Webhook] New token for {customer_email}: {token}")
        # TODO: optionally send token to customer via email
        return "Token issued", 200

    return "Ignored", 200

@app.route('/')
def home():
    return "✅ PayHere Token Backend Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
