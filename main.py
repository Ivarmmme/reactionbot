from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from collections import defaultdict

# Specify the user IDs you want to track
SPECIFIED_USERS = {123456789, 987654321}  # Replace with actual user IDs

message_counts = defaultdict(int)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I will start tracking messages from specified users.')

async def count_messages(update: Update, context: CallbackContext) -> None:
    # Check if the update contains a message
    if update.message:
        user_id = update.message.from_user.id
        if user_id in SPECIFIED_USERS:
            message_counts[user_id] += 1

async def rankings(update: Update, context: CallbackContext) -> None:
    ranked_users = [(user_id, count) for user_id, count in message_counts.items() if user_id in SPECIFIED_USERS]
    ranked_users.sort(key=lambda item: item[1], reverse=True)
    
    ranking_text = 'Message Rankings (Specified Users):\n'
    for user_id, count in ranked_users:
        ranking_text += f'User {user_id}: {count} messages\n'
    
    await update.message.reply_text(ranking_text)

async def error_handler(update: object, context: CallbackContext) -> None:
    # Log the error
    print(f"An error occurred: {context.error}")

def main() -> None:
    application = Application.builder().token('YOUR_TOKEN').build()

    start_handler = CommandHandler('start', start)
    count_handler = MessageHandler(filters.TEXT & filters.ChatType.GROUPS, count_messages)
    rankings_handler = CommandHandler('rankings', rankings)

    application.add_handler(start_handler)
    application.add_handler(count_handler)
    application.add_handler(rankings_handler)

    # Register the error handler
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
