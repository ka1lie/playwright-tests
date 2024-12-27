import sqlite3
import os
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

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
