import random
import json
from config import get_db_connection
from decimal import Decimal

def spin_slot_machine(user_id, bet_amount):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT balance FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()

        if user is None:
            return {"message": "User not found"}, 404

        balance = Decimal(user[0])  # Ensure balance is handled as Decimal

        # Check if the user has enough balance to make the bet
        if balance < Decimal(bet_amount):
            return {"message": "Insufficient balance"}, 400

        # Simulate a slot machine spin using image file paths instead of emojis
        fruits = ['banana.png', 'cherry.png', 'diamond.png', 'grapes.png', 'lemon.png']
        result = [random.choice(fruits) for _ in range(3)]  # Generate 3 random fruits

        # Determine win condition: All fruits must match
        win = 0
        if result[0] == result[1] == result[2]:  # If all three fruits match
            win = bet_amount * 2  # Payout double the bet amount
            new_balance = balance + win  # Update user's balance with the win
        else:
            new_balance = balance - bet_amount

        # Update the user's balance in the database
        cursor.execute('UPDATE users SET balance = %s WHERE user_id = %s', (new_balance, user_id))

        # Store the spin result as a JSON string
        result_json = json.dumps(result)

        # Record the game result in the game history table
        cursor.execute('INSERT INTO game_history (user_id, spin_result, win, bet_amount) VALUES (%s, %s, %s, %s)',
                       (user_id, result_json, win, bet_amount))  # Store result as JSON
        connection.commit()

        return {"spin_result": result, "win": win, "balance": new_balance}

    except Exception as e:
        return {"message": f"Error occurred: {str(e)}"}, 500

    finally:
        cursor.close()
        connection.close()