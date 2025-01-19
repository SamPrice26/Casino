-- Create the new database
-- CREATE DATABASE casino_db;

-- create database
USE casino_db;

-- Create the `users` table with `password_hash` column for storing hashed passwords
-- CREATE TABLE users (
--     user_id INT AUTO_INCREMENT PRIMARY KEY,  
--     username VARCHAR(255) NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,  -- This column stores the hashed password
--     balance DECIMAL(10, 2) DEFAULT 0  -- Ensure a starting balance of 0
-- );

-- Create the `game_history` table with the required fields
-- CREATE TABLE game_history (
--     game_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT,
--     spin_result JSON,  -- Store results as a JSON array
--     win DECIMAL(10, 2),
--     bet_amount DECIMAL(10, 2),
--     FOREIGN KEY (user_id) REFERENCES users(user_id)
-- );

-- UPDATE users SET balance = 100 WHERE user_id = 1;

