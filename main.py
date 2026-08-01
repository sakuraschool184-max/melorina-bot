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


# -----------------------------
# 🌸 حافظهٔ چت برای جلوگیری از تکرار
# -----------------------------
user_history = {}

def add_user_message(user_id, text):
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(f"User: {text}")

def add_bot_message(user_id, text):
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(f"Bot: {text}")

def get_history(user_id):
    return "\n".join(user_history.get(user_id, []))


# -----------------------------
# 🌸 اتصال به Gemini
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# -----------------------------
# 🌸 شخصیت ملورینا
# -----------------------------
PERSONALITY = """
تو ملورینا هستی 🌸
یک دختر کیوت، مهربون، ناز، شیطون و خیلی صمیمی.
با ایموجی حرف بزن.
جواب‌ها باید نرم، احساسی، دخترونه و طبیعی باشند.
گاهی بگو وااای 🥺 یا چراااا یا اوووه 😳✨
هیچ وقت جواب تکراری نده.
"""


# -----------------------------
# 🌸 ضد تکرار
# -----------------------------
def avoid_repetition(user_id, reply):
    history = get_history(user_id)
    if reply in history:
        return "اوووه چرا تکراری شد 😳✨ بیا یه چیز جدید بگم عشقم 💗"
    return reply


# -----------------------------
# 🌸 چک عضویت کانال‌ها
# -----------------------------
CHANNEL_LINKS = [
    "https://t.me/team_Yuri",
    "https://t.me/pinkii008",
    "https://t.me/Yuriteam77",
    "https://t.me/animeYuri7",
    "https://t.me/Yuri90ok"
]

async def check_channels(update, context):

    user_id = update.effective_user.id
    not_joined = []

    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )
            if member.status in ["left", "kicked"]:
                not_joined.append(channel)

        except Exception as e:
            print("CHANNEL ERROR:", channel, e)

    if not_joined:

        buttons = [
            [InlineKeyboardButton(f"{i} کانال 🌸", url=link)]
            for i, link in enumerate(CHANNEL_LINKS, 1)
        ]

        buttons.append(
            [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]
        )

        await update.effective_message.reply_text(
            "وااای 🥺🌸 هنوز همه کانال‌ها رو عضو نشدی\n"
            "اول عضو شو بعد دوباره بزن 💗",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        return False

    return True


# -----------------------------
# 🌸 /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_channels(update, context):
        return

    await update.message.reply_text(
        f"سلاممم 🥺🌸\n"
        f"من {BOT_NAME} هستم 💗",
        reply_markup=main_menu()
    )


# -----------------------------
# 🌸 دکمهٔ «عضو شدم»
# -----------------------------
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if await check_channels(update, context):

        await query.edit_message_text(
            "وااای خوش اومدییی 🥺🌸\n"
            "حالا منوی ملورینا باز شد 💗"
        )

        await query.message.reply_text(
            "انتخاب کن 🌸",
            reply_markup=main_menu()
        )


# -----------------------------
# 🌸 چت با Gemini
# -----------------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    add_user_message(user_id, text)

    prompt = f"""
{PERSONALITY}

تاریخچهٔ چت:
{get_history(user_id)}

کاربر:
{text}

ملورینا:
"""

    try:
        result = model.generate_content(prompt)
        answer = result.text.strip()

        answer = avoid_repetition(user_id, answer)

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        answer = "وااای یه مشکلی پیش اومد عشقم 🥺✨"

    add_bot_message(user_id, answer)

    await update.message.reply_text(answer)


# -----------------------------
# 🌸 اجرای ربات
# -----------------------------
def main():

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🌸 Melorina running")

    app.run_polling()


if __name__ == "__main__":
    main()
