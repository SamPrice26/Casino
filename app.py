from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
from user import register_user, login_user, get_balance, update_balance  # Assume update_balance is added in user.py
from game import spin_slot_machine
import os

app = Flask(__name__)

# Enable CORS for all routes from frontend origin (http://127.0.0.1:5500)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500", "methods": ["GET", "POST", "OPTIONS"]}})


# Serve HTML files from 'static' folder
@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)


@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        return register_user(username, password)
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"message": "An error occurred during registration."}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        return login_user(username, password)
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "An error occurred during login."}), 500


@app.route('/balance/<user_id>', methods=['GET'])
def balance(user_id):
    try:
        return get_balance(user_id)
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return jsonify({"message": "An error occurred while fetching balance."}), 500


@app.route('/spin', methods=['POST'])
def spin():
    try:
        user_id = request.json.get('user_id')
        bet_amount = request.json.get('bet_amount')

        if not user_id or not bet_amount:
            return jsonify({"message": "User ID and bet amount are required"}), 400

        if bet_amount <= 0:
            return jsonify({"message": "Bet amount must be greater than 0"}), 400

        return spin_slot_machine(user_id, bet_amount)
    except Exception as e:
        print(f"Error during spin: {e}")
        return jsonify({"message": "An error occurred during the spin operation."}), 500


# New route to handle claiming the prize
@app.route('/claim-prize', methods=['POST'])
def claim_prize():
    try:
        user_id = request.json.get('user_id')  # Assuming the user ID is passed in the body of the request

        if not user_id:
            return jsonify({"message": "User ID is required"}), 400

        # Logic to add £5 to the user's balance
        new_balance = update_balance(user_id, 5)  # Assuming update_balance function exists and adds the prize

        # Return the updated balance in the response
        return jsonify({
            'message': 'Prize claimed successfully!',
            'new_balance': new_balance
        })
    except Exception as e:
        print(f"Error claiming prize: {e}")
        return jsonify({"message": "An error occurred while claiming the prize."}), 500


if __name__ == '__main__':
    app.run(debug=True)