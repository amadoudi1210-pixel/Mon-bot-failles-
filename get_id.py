from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8492947598:AAH7fk_W8mtjfQL4m7BtNeOJbcDCtqISyHU"

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("CHAT ID =", update.effective_chat.id)
    await update.message.reply_text(f"ID: {update.effective_chat.id}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, get_id))
app.run_polling()
