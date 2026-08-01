import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TELEGRAM_TOKEN, GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)


model = genai.GenerativeModel(
    "gemini-1.5-flash"
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "سلام 🌸 ملورینا آماده چته"
    )



async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text


    try:

        response = model.generate_content(
            user_text
        )


        await update.message.reply_text(
            response.text
        )


    except Exception as e:

        print("GEMINI ERROR:")
        print(repr(e))


        await update.message.reply_text(
            "مشکل از اتصال جمینای هست 🥺"
        )



def main():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    print("BOT RUNNING")

    app.run_polling()



if __name__ == "__main__":
    main()
