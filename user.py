import bcrypt
from flask import jsonify
from config import get_db_connection

# Register User Function
def register_user(username, password):
    if not password:
        return jsonify({"message": "Password cannot be empty"}), 400
    
    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"message": "Username already taken. Please choose a different one."}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()

        user_id = cursor.lastrowid  # Get the ID of the newly created user

        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        connection.close()

# Login User Function
def login_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT user_id, password_hash FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"message": "Invalid username or password"}), 401

        stored_hash = user[1]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return jsonify({"message": "Login successful", "user_id": user[0]}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        connection.close()

# Get User Balance Function
def get_balance(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT balance FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()

        if user:
            return jsonify({"balance": user[0]}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        connection.close()

# Update User Balance Function (for claiming the prize)
def update_balance(user_id, amount):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Get the current balance of the user
        cursor.execute('SELECT balance FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()

        if user:
            # Add the prize amount to the current balance
            new_balance = user[0] + amount

            # Update the user's balance in the database
            cursor.execute('UPDATE users SET balance = %s WHERE user_id = %s', (new_balance, user_id))
            connection.commit()

            return new_balance
        else:
            return None

    except Exception as e:
        print(f"Error updating balance: {str(e)}")
        return None

    finally:
        cursor.close()
        connection.close()