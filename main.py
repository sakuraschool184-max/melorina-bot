import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

from config import (
    TELEGRAM_TOKEN,
    GEMINI_API_KEY,
    BOT_NAME
)
from keyboards import main_menu, join_channels

# اتصال به Gemini
genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


# شخصیت ملورینا
PERSONALITY = """
تو ملورینا هستی 🌸
یک ربات کیوت و صمیمی.
مثل یک دوست مهربون حرف بزن.
جواب‌ها تکراری نباشند.
از ایموجی استفاده کن.
گاهی بگو چراااا 🥺 یا وااای 🌸
خشک و رسمی جواب نده.
"""


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        f"سلاممم 🥺🌸\n"
        f"من {BOT_NAME} هستم 💗\n"
        f"خوش اومدی، بیا باهم حرف بزنیم 🧸"
    )



async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_text = update.message.text


    prompt = f"""
{PERSONALITY}

کاربر گفت:
{user_text}

جواب ملورینا:
"""


    response = model.generate_content(
        prompt
    )


    await update.message.reply_text(
        response.text
    )



def main():

    app = (
        Application
        .builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT,
            chat
        )
    )


    print("Melorina is running 🌸")

    app.run_polling()



if __name__ == "__main__":
    main()
