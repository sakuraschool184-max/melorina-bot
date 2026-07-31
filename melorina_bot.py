import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random

# ========== توکن ربات ==========
TOKEN = "8871217204:AAHC3wYlJEpoOrmOjgt5YN9ShrTBbNgUxrg"

# ========== لیست کانال‌ها ==========
REQUIRED_CHANNELS = [
    "@animeYuri7",
    "@Yuriteam77",
    "@pinkii008",
    "@team_Yuri",
    "@Yuri90ok"
]

# ========== تنظیمات لاگ ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== جواب‌های ملورینا ==========
RESPONSES = [
    "🌸 سلام عزیزم! چطوری؟ 🥰",
    "💫 چه خوب که اومدی! دلم برات تنگ شده بود!",
    "🥰 سلام! چه خبر؟ یه چیز قشنگ بگو!",
    "🌸 به من بگو! هر چی دوست داری! 💕",
    "✨ سلام! آماده‌ای یه ماجراجویی جدید؟ 🎀"
]

# ========== دکمه‌های منو ==========
def get_menu():
    keyboard = [
        [InlineKeyboardButton("💬 چت با ملورینا", callback_data="chat")],
        [InlineKeyboardButton("🌸 کانال انیمه", url="https://t.me/animeYuri7")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== چک کردن عضویت کانال ==========
async def check_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    not_member = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_member.append(channel)
        except:
            not_member.append(channel)
    
    return not_member

# ========== دستور start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # چک کردن عضویت
    not_member = await check_channels(update, context)
    
    if not_member:
        keyboard = []
        for ch in not_member:
            clean_ch = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 عضویت در {ch}", url=f"https://t.me/{clean_ch}")])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        
        await update.message.reply_text(
            f"🌸 سلام {user.first_name} عزیزم! 🥰\n\n"
            f"برای استفاده از ربات، باید تو این کانال‌ها عضو بشی:\n\n"
            f"{chr(10).join([f'• {ch}' for ch in not_member])}\n\n"
            f"✨ بعد از عضویت، دکمه بررسی رو بزن! 💫",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # اگه همه عضویت‌ها کامل بود
    await update.message.reply_text(
        f"🌸 سلام {user.first_name}! 🥰\n\n"
        f"من ملورینا هستم! 😍\n"
        f"هر چی دوست داری بپرس! 💫",
        reply_markup=get_menu()
    )

# ========== دکمه بررسی مجدد ==========
async def check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    not_member = await check_channels(update, context)
    
    if not_member:
        keyboard = []
        for ch in not_member:
            clean_ch = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 عضویت در {ch}", url=f"https://t.me/{clean_ch}")])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        
        await query.edit_message_text(
            f"🌸 هنوز عضو نشدی عزیزم! 🥺\n"
            f"این کانال‌ها رو عضو شو:\n\n"
            f"{chr(10).join([f'• {ch}' for ch in not_member])}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(
            "🌸 تبریک! همه کانال‌ها رو عضو شدی! 🥰\n\n"
            "حالا می‌تونی از من هر چی دوست داری بپرسی! 💫",
            reply_markup=get_menu()
        )

# ========== چت با ملورینا ==========
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_message.startswith('/'):
        return
    
    # چک کردن عضویت
    not_member = await check_channels(update, context)
    if not_member:
        keyboard = []
        for ch in not_member:
            clean_ch = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 عضویت در {ch}", url=f"https://t.me/{clean_ch}")])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        
        await update.message.reply_text(
            f"🌸 عزیزم! هنوز تو کانال‌ها عضو نشدی! 🥺",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # جواب دادن
    reply = random.choice(RESPONSES)
    await update.message.reply_text(reply, reply_markup=get_menu())

# ========== دکمه چت ==========
async def chat_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "💬 **چت با ملورینا** 💬\n\n"
        "🌸 هر چی دوست داری بپرس! 🥰\n"
        "من گوش می‌دم! 💫",
        reply_markup=get_menu(),
        parse_mode="Markdown"
    )

# ========== منوی اصلی ==========
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🌸 **منوی اصلی** 🥰\n\n"
        "چی دوست داری؟ 💫",
        reply_markup=get_menu(),
        parse_mode="Markdown"
    )

# ========== اجرا ==========
def main():
    app = Application.builder().token(TOKEN).build()
    
    # دستورات
    app.add_handler(CommandHandler("start", start))
    
    # پیام‌های متنی (چت)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    # دکمه‌ها
    app.add_handler(CallbackQueryHandler(check_again, pattern="check_again"))
    app.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))
    app.add_handler(CallbackQueryHandler(chat_button, pattern="chat"))
    
    print("🌸 ملورینا روشن شد! 🥰")
    print("=" * 40)
    print("✅ چک کردن ۵ کانال")
    print("✅ چت ساده با ملورینا")
    print("✅ دکمه‌های ساده")
    print("=" * 40)
    
    app.run_polling()

if __name__ == "__main__":
    main()
