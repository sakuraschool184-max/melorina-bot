import os
import logging
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

# ====== تنظیم لاگ ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== گرفتن کلیدها ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN پیدا نشد!")
if not GEMINI_KEY:
    raise ValueError("❌ GEMINI_API_KEY پیدا نشد!")

# ====== لیست کانال‌ها (با @ یا عددی) ======
CHANNELS = [
    "@team_Yuri",
    "@pinkii008",
    "@Yuriteam77", 
    "@animeYuri7",
    "@Yuri90ok"
]

# ====== تنظیم Gemini ======
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
logger.info("🌸 Gemini آماده شد!")

# ====== تابع چک کردن عضویت ======
async def check_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    not_joined = []
    
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_joined.append(channel)
        except Exception as e:
            logger.error(f"خطا در چک کردن {channel}: {e}")
            not_joined.append(channel)
    
    if not_joined:
        buttons = []
        for ch in not_joined:
            # ساخت لینک صحیح
            if ch.startswith("@"):
                link = f"https://t.me/{ch[1:]}"
            else:
                link = f"https://t.me/{ch}"
            
            buttons.append([InlineKeyboardButton(f"🌸 عضو شو", url=link)])
        
        buttons.append([InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")])
        
        await update.message.reply_text(
            "🌸 سلام عزیزم! 💕\n\n"
            "برای استفاده از ملورینا، اول باید عضو این کانال‌های قشنگ بشی 🎀\n"
            "روی دکمه‌های زیر بزن و عضو شو، بعد بزن **عضو شدم** ✨",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode='Markdown'
        )
        return False
    
    return True

# ====== تابع استارت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_channels(update, context):
        return
    
    keyboard = [
        [InlineKeyboardButton("🌸 درباره من", callback_data="about")],
        [InlineKeyboardButton("💕 راهنما", callback_data="help")],
        [InlineKeyboardButton("🎀 وبسایت", url="https://github.com")]
    ]
    
    await update.message.reply_text(
        "✨ سلام عزیزم! ✨\n\n"
        "من **ملورینا** هستم 🌸\n"
        "یه ربات کیوت که عاشق کمک به توئه! 💕\n\n"
        "هر چی دوست داری ازم بپرس! 🎀",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ====== مدیریت دکمه‌ها ======
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "about":
        await query.edit_message_text(
            "🌸 درباره من:\n\n"
            "من ملورینا هستم، یه ربات کیوت با قلب مهربون! ✨\n"
            "با هوش مصنوعی Gemini ساخته شدم تا بتونم بهت کمک کنم.\n\n"
            "هدفم اینه که روزت رو قشنگ‌تر کنم! 💕"
        )
    elif query.data == "help":
        await query.edit_message_text(
            "💕 راهنما:\n\n"
            "🌸 فقط سوالت رو بپرس!\n"
            "💡 هر چیزی می‌تونی بپرسی:\n"
            "• سوالات علمی 🔬\n"
            "• کمک درسی 📚\n"
            "• ایده‌پردازی 🎨\n"
            "• یا یه گپ ساده 🫂"
        )

# ====== چک کردن عضویت بعد از کلیک ======
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    not_joined = []
    
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel)
    
    if not_joined:
        buttons = []
        for ch in not_joined:
            if ch.startswith("@"):
                link = f"https://t.me/{ch[1:]}"
            else:
                link = f"https://t.me/{ch}"
            buttons.append([InlineKeyboardButton(f"🌸 عضو شو", url=link)])
        
        buttons.append([InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")])
        
        await query.edit_message_text(
            "🥺 هنوز همه کانال‌ها رو عضو نشدی عزیزم!\n"
            "روی دکمه‌ها بزن و عضو شو 💕",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await query.edit_message_text(
            "🎉 وااای خوش اومدییی! 🥺🌸\n"
            "حالا می‌تونیم با هم حرف بزنیم 💗\n"
            "هر چی دوست داری بپرس! ✨"
        )

# ====== پاسخ به پیام‌ها با Gemini ======
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # اول چک کن عضو هست یا نه
    if not await check_channels(update, context):
        return
    
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    # پیام تایپ
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    prompt = f"""
تو ملورینا هستی 🌸
یه ربات خیلی کیوت و مهربون با شخصیت شیرین.
با ایموجی‌های قشنگ جواب بده.
جواب‌ها تکراری نباشن و همیشه پر انرژی باشی.

کاربر: {user_message}

ملورینا:
"""
    
    try:
        result = model.generate_content(prompt)
        answer = result.text if result.text else "🌸 یه چیزی بگم؟ راستش نتونستم جوابتو پیدا کنم! ولی بازم دوستت دارم 💕"
    except Exception as e:
        logger.error(f"خطا در Gemini: {e}")
        answer = "🥺 واای! یه مشکل کوچیک توی جادوی من پیش اومد! لطفاً دوباره تلاش کن عزیزم 💗"
    
    await update.message.reply_text(answer)

# ====== اجرای ربات ======
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(about|help)$"))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    logger.info("🌸 ملورینا روشن شد! ✨")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
