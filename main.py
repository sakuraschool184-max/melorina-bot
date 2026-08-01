import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(
    api_key=GEMINI_KEY
)


model = genai.GenerativeModel(
    "gemini-1.5-flash"
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "سلاممم 🥺🌸\n"
        "من ملورینا هستم 💗\n"
        "بیا حرف بزنیم 🧸"
    )



async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    try:

        result = model.generate_content(
            text
        )

        answer = result.text


    except Exception as e:

        print("FULL GEMINI ERROR:", repr(e))

        answer = (
            "وااای 🥺🌸\n"
            "یه مشکل کوچولو توی جادوی من پیش اومد 💗"
        )


    await update.message.reply_text(
        answer
    )



def main():

    app = Application.builder().token(
        BOT_TOKEN
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


    print("🌸 Melorina is running")

    app.run_polling()



if __name__ == "__main__":
    main()
