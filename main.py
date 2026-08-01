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

from config import TELEGRAM_TOKEN, GEMINI_API_KEY, BOT_NAME, CHANNELS
from keyboards import main_menu


# اتصال Gemini
genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


PERSONALITY = """
تو ملورینا هستی 🌸
یک ربات کیوت و دوست داشتنی.
مثل یک دوست صمیمی حرف بزن.
از ایموجی استفاده کن.
گاهی بگو وااای 🥺 یا چراااا 🌸
جواب‌ها تکراری نباشند.
"""


# لینک‌های کانال برای دکمه‌ها
CHANNEL_LINKS = [
    "https://t.me/team_Yuri",
    "https://t.me/pinkii008",
    "https://t.me/Yuriteam77",
    "https://t.me/animeYuri7",
    "https://t.me/Yuri90ok"
]


# بررسی عضویت
async def check_channels(update, context):

    user_id = update.effective_user.id
    not_joined = []


    for channel in CHANNELS:

        try:

            member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )


            if member.status in [
                "left",
                "kicked"
            ]:
                not_joined.append(channel)


        except Exception as e:

            print(
                "CHANNEL ERROR:",
                channel,
                e
            )


    if not_joined:


        buttons = []


        for i, link in enumerate(CHANNEL_LINKS, 1):

            buttons.append(
                [
                    InlineKeyboardButton(
                        f"①②③④⑤"[i-1] + " کانال 🌸",
                        url=link
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


        await update.effective_message.reply_text(
            "وااای 🥺🌸 هنوز همه کانال‌های یوری رو عضو نشدی\n\n"
            "برای استفاده از ملورینا اول این پنج کانال رو دنبال کن 💗",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


        return False


    return True



# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if not await check_channels(update, context):
        return


    await update.message.reply_text(
        f"سلاممم 🥺🌸\n"
        f"من {BOT_NAME} هستم 💗\n"
        f"خوش اومدی، بیا باهم حرف بزنیم 🧸",
        reply_markup=main_menu()
    )



# چت با Gemini
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if not await check_channels(update, context):
        return


    text = update.message.text


    prompt = f"""
{PERSONALITY}

کاربر گفت:
{text}

جواب ملورینا:
"""


    try:

        result = model.generate_content(prompt)

        answer = result.text


    except Exception as e:

        print(
            "GEMINI ERROR:",
            e
        )

        answer = (
            "وااای 🥺🌸 یه مشکل کوچولو پیش اومد\n"
            "دوباره امتحان کن 💗"
        )


    await update.message.reply_text(
        answer
    )



# دکمه عضو شدم
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):


    query = update.callback_query

    await query.answer()


    if await check_channels(update, context):

        await query.edit_message_text(
            "وااای خوش اومدییی 🥺🌸\n"
            "حالا می‌تونی با ملورینا حرف بزنی 💗"
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


    print(
        "🌸 Melorina is running"
    )


    app.run_polling()



if __name__ == "__main__":
    main()
