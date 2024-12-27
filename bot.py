import sqlite3
import os
import requests
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# импортируем переменные из dotenv
load_dotenv()

# Predefined password (use environment variables or secure hashing in production)
#PASSWORD = "mysecretpassword"

# Initialize the SQLite3 database to store user info
def create_db():
    conn = sqlite3.connect('/root/sqlite3/telegram.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            email TEXT,
            telegram_id INTEGER PRIMARY KEY,            
            phone_number TEXT,
            is_authorized INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Store user information (including authorization status) in the database
def store_user_data(telegram_id, username, phone_number, is_authorized):
    conn = sqlite3.connect('/root/sqlite3/telegram.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (telegram_id, username, phone_number, is_authorized)
        VALUES (?, ?, ?, ?)
    ''', (telegram_id, username, phone_number, is_authorized))
    conn.commit()
    conn.close()


# Function to check if the external service returns the expected JSON data
def check_external_service():
    url = os.getenv('URL')  # Replace with your actual URL

    try:
        response = requests.get(url)
        # If the response is successful and contains JSON
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            # Define the expected JSON structure (Example)
            expected_data = {
                "status": "success",
            }

            # Compare the actual data with the expected values
            if data.get("status") == expected_data["status"]:
                logger.info("External service returned expected data.")
                return True
            else:
                logger.warning(f"External service returned unexpected data: {data}")
                return False
        else:
            logger.error(f"Failed to fetch data. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return False


# Start command handler
def start(update: Update, context: CallbackContext):
    # Ask for the password to authenticate
    update.message.reply_text("Please enter the password to access the bot:")

# Handle password input and request user information after authentication
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # Check if the user is already authorized
    conn = sqlite3.connect('/root/sqlite3/telegram.db')
    cursor = conn.cursor()
    cursor.execute("SELECT is_authorized FROM users WHERE telegram_id = ?", (user_id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        update.message.reply_text("You are already authorized.")
        conn.close()
        return

    # Check the entered password
    if update.message.text == os.getenv('PASSWORD'):
        # Mark the user as authorized
        store_user_data(user_id, username, "", 1)
        update.message.reply_text("Password correct! Now please share your phone number.")

        # Send a button to request the phone number
        keyboard = [[KeyboardButton("Send my phone number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text("Click the button to send your phone number:", reply_markup=reply_markup)
        if result and result[0] == 1:
            update.message.reply_text("You are already authorized.")
            conn.close()
            return
    else:
        update.message.reply_text("Incorrect password. Please try again.")
        conn.close()

# Handle the contact (phone number) message
def handle_contact(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    phone_number = update.message.contact.phone_number

    # Retrieve the username and update the database
    username = update.message.from_user.username
    store_user_data(user_id, username, phone_number, 1)

    update.message.reply_text(f"Thank you! Your username: {username}, Phone number: {phone_number} have been saved.")


async def notify_authorized_users():
    if not check_external_service():
        conn = sqlite3.connect('/root/sqlite3/telegram.db')
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id FROM users WHERE authorized = 1")  # Get all authorized users
        authorized_users = cursor.fetchall()
        conn.close()

        # Notify all authorized users about the unexpected service data
        for user_id, in authorized_users:
            try:
                bot.send_message(user_id, "Alert: The external service returned unexpected data!")
#                logger.info(f"Notified user {user_id} about the unexpected data.")
            except Exception as e:
                print(f"Failed to send notification to {user_id}: {e}")


# Main function to run the bot
def main():
    # Initialize the bot with your token
    updater = Updater(os.getenv('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    # Create the database if it doesn't exist
    create_db()

    # Add handlers for commands and messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.contact, handle_contact))

    notify_authorized_users()

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
