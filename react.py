import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio 

# Replace with your Telegram bot token 
YOUR_BOT_TOKEN = "7116973701:AAHkNxvQqS85ko0sBtQ_QoVM90UKfzAOgco" 

# Replace with the ID of the user you want to react to
target_user_id = 6369933143 

async def react_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == target_user_id:
        await context.bot.send_reaction(chat_id=update.message.chat_id, 
                                        message_id=update.message.message_id,
                                        emoji='👍') 

async def main():
    application = Application.builder().token(YOUR_BOT_TOKEN).build()

    await application.initialize() # Add this line!

    application.add_handler(MessageHandler(filters.TEXT, react_to_user))

    await application.start()
    await application.idle()

