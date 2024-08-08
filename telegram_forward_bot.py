from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Define stages
SOURCE_CHANNEL, TARGET_CHANNEL = range(2)

# Dictionary to store user channel selections
user_data = {}

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Welcome! Use /forward to start forwarding messages between channels.')
    return ConversationHandler.END

def forward_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please send me the username or ID of the source channel.')
    return SOURCE_CHANNEL

def source_channel(update: Update, context: CallbackContext) -> int:
    user_data['source_channel'] = update.message.text
    update.message.reply_text('Got it! Now, please send me the username or ID of the target channel.')
    return TARGET_CHANNEL

def target_channel(update: Update, context: CallbackContext) -> int:
    user_data['target_channel'] = update.message.text
    update.message.reply_text('Channels set! I will now forward messages from the source channel to the target channel.')
    
    # Save the source and target channels in context
    context.user_data['source_channel'] = user_data['source_channel']
    context.user_data['target_channel'] = user_data['target_channel']
    
    return ConversationHandler.END

def forward_messages(update: Update, context: CallbackContext) -> None:
    source_channel = context.user_data.get('source_channel')
    target_channel = context.user_data.get('target_channel')
    
    if update.message.chat.username == source_channel:
        context.bot.forward_message(chat_id=target_channel, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    updater = Updater("7115819609:AAE9MvU9-RN0E-ccOGB6HO1YdbcGETFuchc")
    
    dp = updater.dispatcher

    # Conversation handler for /forward command
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('forward', forward_command)],
        states={
            SOURCE_CHANNEL: [MessageHandler(Filters.text & ~Filters.command, source_channel)],
            TARGET_CHANNEL: [MessageHandler(Filters.text & ~Filters.command, target_channel)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
