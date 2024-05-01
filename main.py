import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler 
import asyncio 
import json  # For storing seen messages in a JSON file

# ----------------- Configuration ----------------- 
YOUR_BOT_TOKEN = "7116973701:AAHkNxvQqS85ko0sBtQ_QoVM90UKfzAOgco" 
TARGET_USER_ID = 6369933143 
STORAGE_FILE = "seen_messages.json" 
# -----------------------------------------------

# Load previously seen message IDs
try:
    with open(STORAGE_FILE, "r") as f:
        seen_message_ids = json.load(f)
except FileNotFoundError:
    seen_message_ids = []

async def react_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reacts to new messages from the target user."""

    message_id = update.message.message_id
    if update.message.from_user.id == TARGET_USER_ID and message_id not in seen_message_ids:
        await context.bot.send_reaction(chat_id=update.message.chat_id, 
                                        message_id=message_id,
                                        emoji='👍') 
        seen_message_ids.append(message_id)
        save_seen_messages()

def save_seen_messages():
    """Saves the list of seen message IDs to the storage file."""

    with open(STORAGE_FILE, "w") as f:
        json.dump(seen_message_ids, f)

async def main():
    """Bot setup and initialization."""

    application = Application.builder().token(YOUR_BOT_TOKEN).build()
    await application.initialize() 

    application.add_handler(MessageHandler(None, react_to_user))  # React to all message types

    await application.start()
    await application.idle()

if __name__ == '__main__':
    asyncio.run(main()) 
