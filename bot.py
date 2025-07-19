from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
from config import BOT_TOKEN, SHRINKME_API_KEY, SOURCE_BOT_USERNAME

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome to Rozi Bot!\nSearch for any movie in @movielockerhau group.")

async def handle_get_link(update: Update, context: CallbackContext):
    query = update.callback_query
    movie_name = query.data.split(":", 1)[1]
    short_url = get_shortlink(f"https://t.me/{SOURCE_BOT_USERNAME}?start={movie_name.replace(' ', '_')}")
    
    if short_url:
        await query.message.reply_text(f"🔗 Please verify using this link:\n{short_url}")
        await query.message.reply_text("✅ Once verified, reply /done")
    else:
        await query.message.reply_text("❌ Failed to generate link.")

def get_shortlink(original_url):
    api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={original_url}"
    try:
        res = requests.get(api_url).json()
        return res["shortenedUrl"]
    except:
        return None

async def done(update: Update, context: CallbackContext):
    await update.message.reply_text("🎬 Here is your movie!")
    await context.bot.forward_message(
        chat_id=update.message.chat_id,
        from_chat_id="@Bollyhollyhub",
        message_id=123  # You will replace with real logic later
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CallbackQueryHandler(handle_get_link, pattern="^getlink:"))

    print("Bot is alive 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
