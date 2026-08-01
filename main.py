import os
import google.generativeai as genai

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


CHANNELS = [
    "https://t.me/team_Yuri",
    "https://t.me/pinkii008",
    "https://t.me/Yuriteam77",
    "https://t.me/animeYuri7",
    "https://t.me/Yuri90ok"
]


print("Gemini key موجوده:", bool(GEMINI_KEY))


genai.configure(
    api_key=GEMINI_KEY
)


try:
    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )
    print("Gemini آماده شد 🌸")

except Exception as e:
    print("Gemini setup error:", e)



async def check_channels(update, context):

    user_id = update.effective_user.id

    not_joined = []


    for ch in CHANNELS:

        try:

            member = await context.bot.get_chat_member(
                chat_id=ch,
                user_id=user_id
            )


            if member.status in [
                "left",
                "kicked"
            ]:
                not_joined.append(ch)


        except Exception as e:

            print("Channel check error:", e)
            not_joined.append(ch)



    if not_joined:

        buttons = []


        for i, ch in enumerate(not_joined, 1):

            buttons.append(
                [
                    InlineKeyboardButton(
                        f"کانال {i} 🌸",
                        url=ch
                    )
                ]
            )


        buttons.append(
            [
                InlineKeyboardButton(
                    "✅ عضو شدم",
                    callback_data="check_join"
                )
            ]
        )


        await update.message.reply_text(
            "وااای 🥺🌸 هنوز پنج کانال یوری رو عضو نشدی 💗\n\n"
            "اول عضو شو بعد دوباره امتحان کن ✨",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        return False


    return True




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_channels(update, context):
        return


    await update.message.reply_text(
        "سلاممم 🥺🌸\n"
        "من ملورینا هستم 💗\n"
        "بیا باهم حرف بزنیم 🧸"
    )




async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    if await check_channels(update, context):

        await query.edit_message_text(
            "وااای خوش اومدییی 🥺🌸\n"
            "حالا می‌تونیم حرف بزنیم 💗"
        )




async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    prompt = f"""
تو ملورینا هستی 🌸
یک ربات خیلی کیوت و مهربون هستی.
با ایموجی جواب بده.
جواب‌ها تکراری نباشند.

کاربر:
{text}

جواب:
"""


    try:

        result = model.generate_content(
            prompt
        )

        answer = result.text


    except Exception as e:

        print(
            "FULL GEMINI ERROR:",
            repr(e)
        )


        answer = (
            "وااای 🥺🌸 "
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
        CallbackQueryHandler(
            check_join,
            pattern="check_join"
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
