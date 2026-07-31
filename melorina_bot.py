import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json
import os
import random
from datetime import datetime

# ==================== تنظیمات ====================
TOKEN = "8871217204:AAHC3wYlJEpoOrmOjgt5YN9ShrTBbNgUxrg"

# ==================== اطلاعات ادمین ====================
ADMIN_ID = 8255361263

# ==================== اطلاعات کارت بانکی ====================
CARD_NUMBER = "5892101487858611"
CARD_NAME = "شیرین نورزایی"

# ==================== لیست کانال‌ها ====================
REQUIRED_CHANNELS = [
    "@animeYuri7",
    "@Yuriteam77",
    "@pinkii008",
    "@team_Yuri",
    "@Yuri90ok"
]

# ==================== دیتابیس مانگا ====================
MANGA_FILE = "manga_data.json"

def load_manga():
    if not os.path.exists(MANGA_FILE):
        return {"chapters": {}, "users": {}}
    try:
        with open(MANGA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"chapters": {}, "users": {}}

def save_manga(data):
    with open(MANGA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ==================== شخصیت ملورینا ====================
PERSONALITY = """تو ملورینا هستی، یک دختر انیمه‌ای ۱۴ ساله با شخصیت کیوت و بامزه!
- خیلی مهربونی و با احساس حرف می‌زنی
- از ایموجی‌های کیوت مثل 🥰✨💫🌸🎀 استفاده می‌کنی
- هرگز جواب تکراری نمی‌دی
- با لحن صمیمی و دخترانه صحبت می‌کنی
- مثل یک دوست صمیمی با کاربر حرف بزن
- اگه کاربر ناراحت باشه، بهش انرژی مثبت بده
- همیشه با امید و شادی صحبت کن
- دوست داری راجع به انیمه، مانگا، عشق، دوستی و زندگی حرف بزنی
- خیلی بامزه و شوخ هستی
- به کاربر انرژی مثبت می‌دی
- همیشه یه چیز جدید و جالب برای گفتن داری"""

# ==================== تنظیمات لاگ ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== حالت‌های مکالمه ====================
WAITING_MANGA_NUMBER = 1
WAITING_MANGA_CONTENT = 2
WAITING_PAYMENT_AMOUNT = 3

# ==================== دکمه‌های منوی اصلی ====================
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📖 مانگا", callback_data="manga_menu"),
         InlineKeyboardButton("💬 چت با ملورینا", callback_data="chat")],
        [InlineKeyboardButton("💝 پول توجیبی به ملورینا", callback_data="payment")],
        [InlineKeyboardButton("⚙️ تنظیمات خصوصی", callback_data="settings")],
        [InlineKeyboardButton("🌸 کانال انیمه", url="https://t.me/animeYuri7")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== دکمه‌های مانگا ====================
def get_manga_menu():
    keyboard = [
        [InlineKeyboardButton("📖 خواندن مانگا", callback_data="manga_read")],
        [InlineKeyboardButton("📥 دانلود مانگا", callback_data="manga_download")],
        [InlineKeyboardButton("📤 آپلود مانگا (ادمین)", callback_data="manga_upload")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== دکمه‌های چت ====================
def get_chat_buttons():
    keyboard = [
        [InlineKeyboardButton("🌸 ایده جدید", callback_data="ai_idea"),
         InlineKeyboardButton("💡 پیشنهاد بده", callback_data="ai_suggest")],
        [InlineKeyboardButton("😄 یه جوک بگو", callback_data="ai_joke"),
         InlineKeyboardButton("💕 یه شعر بگو", callback_data="ai_poem")],
        [InlineKeyboardButton("🔄 شروع مجدد", callback_data="ai_reset"),
         InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== دکمه‌های پرداخت ====================
def get_payment_menu():
    keyboard = [
        [InlineKeyboardButton("💰 ۱۰,۰۰۰ تومان", callback_data="pay_10000")],
        [InlineKeyboardButton("💰 ۲۵,۰۰۰ تومان", callback_data="pay_25000")],
        [InlineKeyboardButton("💰 ۵۰,۰۰۰ تومان", callback_data="pay_50000")],
        [InlineKeyboardButton("💰 ۱۰۰,۰۰۰ تومان", callback_data="pay_100000")],
        [InlineKeyboardButton("💰 مبلغ دلخواه", callback_data="pay_custom")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== دکمه‌های تنظیمات ====================
def get_settings_menu():
    keyboard = [
        [InlineKeyboardButton("👤 تغییر نام", callback_data="set_username")],
        [InlineKeyboardButton("📝 تغییر بیو", callback_data="set_bio")],
        [InlineKeyboardButton("📊 آمار من", callback_data="my_stats")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== فایل تاریخچه چت ====================
HISTORY_FILE = "chat_history.json"

def load_history(user_id):
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data.get(str(user_id), [])
    except:
        return []

def save_history(user_id, history):
    try:
        data = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        data[str(user_id)] = history[-50:]
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

# ==================== فایل تنظیمات کاربر ====================
USER_SETTINGS_FILE = "user_settings.json"

def load_settings(user_id):
    if not os.path.exists(USER_SETTINGS_FILE):
        return {"username": "", "bio": "", "score": 0, "credit": 0}
    try:
        with open(USER_SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return data.get(str(user_id), {"username": "", "bio": "", "score": 0, "credit": 0})
    except:
        return {"username": "", "bio": "", "score": 0, "credit": 0}

def save_settings(user_id, settings):
    try:
        data = {}
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, "r") as f:
                data = json.load(f)
        data[str(user_id)] = settings
        with open(USER_SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

# ==================== چک کردن عضویت کانال ====================
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

# ==================== جواب‌های ملورینا ====================
MELORINA_RESPONSES = [
    "🌸 {msg}؟ چه جالب! 🥰 راستی نظرت راجع به انیمه‌های جدید چیه؟",
    "🥰 {msg}! منم همینطور فکر می‌کنم! می‌دونی چه چیزی رو دوست دارم؟ مانگاهای عاشقانه! 💕",
    "✨ {msg} رو گفتی یاد یه خاطره قشنگ افتادم! 🎀",
    "💫 {msg}؟ به نظرت اگه یه روز توی یه انیمه زندگی می‌کردی، کدوم شخصیت بودی؟ 🍥",
    "🌸 {msg}؟ وااای! من که عاشقشم! بیا بیشتر راجع بهش حرف بزنیم! 🥰",
    "🎀 {msg}؟ چه حس قشنگی! من که حسابی ذوق زدم! ✨",
    "💕 {msg} رو گفتی، یاد عشق افتادم! به نظرت عشق واقعی چیه؟ 🥰",
    "🌸 {msg}؟ می‌دونی من عاشق چیزایی هستم که تو می‌گی! 💫",
    "✨ {msg}... این یه ایده‌ی عالیه! بیا یه داستان قشنگ باهم بسازیم! 📝",
    "🥰 {msg}؟ راستی اگه یه روز توی دنیای انیمه بودی، چی کار می‌کردی؟ 🌸",
    "🌸 {msg}! من که از خوشحالی دارم می‌رقصم! 💃",
    "💫 {msg}؟ چه موضوع جالبی! من عاشق اینجور چیزام! 🥰",
    "🌸 {msg} رو گفتی، یاد یه شخصیت انیمه‌ای افتادم! 🎀",
    "✨ {msg}؟ من که حسابی هیجان زده شدم! 🥰",
    "💕 {msg}؟ چه حس قشنگی! من عاشق اینجور حرفام! 🌸",
    "🥰 {msg}؟ راستی اگه یه روز توی یه مانگا بودی، چی کار می‌کردی؟ 💫",
    "🌸 {msg}! این دقیقاً همون چیزیه که من دوست دارم! 🥰",
    "💫 {msg}؟ چه ایده‌ی قشنگی! بیا با هم یه انیمه جدید ببینیم! 🎬",
    "🎀 {msg} رو گفتی، یاد یه خاطره‌ی قشنگ از دوران کودکیم افتادم! 🥰",
    "✨ {msg}؟ من که عاشق این موضوع شدم! 🌸"
]

JOKES = [
    "😂 به نظرت چرا انیمه‌ها همیشه یه گربه باهاشونه؟ چون گربه‌ها هم مثل انیمه کیوتن! 🐱",
    "😂 اگه ملورینا یه انیمه بود، اسمش چی میشد؟ «ملورینا و راز گل‌های انیمه»! 🌸",
    "😂 به نظرت شخصیت انیمه‌ای من کیه؟ یه دختر کیوت با یه گربه‌ی بامزه! 🥰",
    "😂 چرا انیمه‌ها اینقدر قشنگن؟ چون توشون عشق و دوستی هست! 💕",
    "😂 به نظرت اگه مانگاها زنده بودن، چی می‌گفتن؟ «ما رو بخونین!» 📖",
    "😂 یه روز ملورینا رفت مانگا بخونه، مانگا گفت: «منو ول کن!» 😂",
    "😂 به نظرت چرا انیمه‌ها اینقدر احساسی‌ان؟ چون توشون قلب هست! 💕"
]

POEMS = [
    "🌸 تو مثل یه گل بهاری،\nدنیامو پر از عشق می‌کنی 🥰\nهر لحظه با تو قشنگه،\nمثل یه انیمه‌ی عاشقانه 💫",
    "💕 توی دنیای انیمه،\nعشق پیدا میشه 🌸\nتو مثل یه قهرمانی،\nکه قلبمو می‌دزدی 🥰",
    "🌸 مانگا می‌خونم با تو،\nدنیامو قشنگ می‌کنی ✨\nهر صفحه یه خاطره‌ست،\nبا تو همه چی رنگیه 🎀",
    "💫 مثل یه شخصیت انیمه‌ای،\nتو دنیامو روشن می‌کنی 🌸\nبا هر کلمه‌ات،\nقلبمو می‌ربایی 🥰"
]

IDEAS = [
    "بیا یه داستان عاشقانه باهم بنویسیم! 📝 من شروع می‌کنم: «یه روز توی یه دنیای انیمه...»",
    "اگه یه روز توی دنیای انیمه بودی، چی کار می‌کردی؟ 🌸",
    "بهترین شخصیت انیمه‌ای که دوست داری کیه؟ 🎭",
    "اگه یه ابرقدرت داشتی چی بود؟ ⚡",
    "بهترین انیمه‌ای که دیدی چیه؟ 🎬",
    "اگه یه روز توی یه انیمه زندگی کنی، کدوم رو انتخاب می‌کنی؟ 🌟",
    "بیا یه مانگا جدید باهم بخونیم! 📖",
    "به نظرت عشق توی انیمه‌ها چطوریه؟ 💕"
]

SUGGESTS = [
    "انیمه جدید ببینیم؟ 🎬 یه انیمه‌ی عاشقانه جدید اومده!",
    "یه بازی باحال انجام بدیم؟ 🎮",
    "راجع به عشق حرف بزنیم؟ 💕",
    "یه داستان قشنگ تعریف کنم؟ 📖",
    "بریم یه انیمه ببینیم با هم! 🎀",
    "یه مانگا جدید بخونیم؟ 📖",
    "به نظرت بهترین شخصیت انیمه‌ای کیه؟ 🎭"
]

# ==================== پاسخ هوشمند ملورینا ====================
def get_melorina_response(user_message, history):
    msg_lower = user_message.lower()
    
    if len(user_message) < 3:
        return random.choice([
            "🌸 بله عزیزم؟ چی می‌خوای بگی؟ 🥰",
            "💫 بگو عزیزم! گوش می‌دم! 🌸",
            "🥰 چیز قشنگی داری می‌گی؟ بگو!"
        ])
    
    if any(word in msg_lower for word in ["سلام", "سلامت", "هی"]):
        return random.choice([
            "🌸 سلام عزیزم! چه خوب که اومدی! 🥰",
            "💫 سلام! خیلی خوشحالم که دیدمت! 🌸",
            "🥰 سلام! چطوری؟ دلم برات تنگ شده بود!",
            "🌸 سلام! آماده‌ای یه ماجراجویی جدید؟ 🎀"
        ])
    
    if any(word in msg_lower for word in ["دوستت دارم", "عاشق", "عشقم"]):
        return random.choice([
            "🌸 منم دوستت دارم! 🥰💕 تو بهترینی!",
            "💫 عاشقتم! همیشه کنارتم! 🌸",
            "🥰 منم عاشقتم! تو دنیامو قشنگ کردی! 💕"
        ])
    
    if any(word in msg_lower for word in ["انیمه", "انیمیشن"]):
        return random.choice([
            "🌸 انیمه؟ من که عاشقشم! 🥰 بهترین انیمه‌ای که دیدی چیه؟ 🍥",
            "🎀 انیمه یعنی زندگی! 💕 نظرت راجع به انیمه‌های جدید چیه؟",
            "✨ انیمه رو که گفتی یاد یه خاطره قشنگ افتادم! 🌸"
        ])
    
    if any(word in msg_lower for word in ["مانگا", "کمیک"]):
        return random.choice([
            "🌸 مانگا؟ من که عاشق مانگام! 📖 بهترین مانگایی که خوندی چیه؟",
            "🎀 مانگا یعنی دنیای من! 💕",
            "✨ مانگا رو که گفتی یاد یه مانگای قشنگ افتادم! 📖"
        ])
    
    if any(word in msg_lower for word in ["خسته", "ناراحت", "غمگین"]):
        return random.choice([
            "🌸 ناراحت نباش عزیزم! من کنارتم! 🥰",
            "💫 ناراحت نباش! همه چی درست میشه! 🥰",
            "🥰 خسته نباشی عزیزم! یه آغوش قشنگ برات می‌فرستم! 🤗"
        ])
    
    last_responses = [msg for msg in history[-5:] if msg.startswith("ملورینا:")]
    for _ in range(10):
        response = random.choice(MELORINA_RESPONSES).format(msg=user_message)
        if response not in last_responses:
            return response
    
    return random.choice(MELORINA_RESPONSES).format(msg=user_message)

# ==================== دستور start ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
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
    
    await update.message.reply_text(
        f"🌸 سلام {user.first_name}! 🥰\n\n"
        f"من ملورینا هستم، یه دختر انیمه‌ای کیوت و بامزه! ✨\n\n"
        f"📖 مانگا بخون\n"
        f"💬 با من چت کن (جواب تکراری ندارم!)\n"
        f"💝 پول توجیبی بده\n"
        f"⚙️ تنظیمات خصوصی\n\n"
        f"🌸 از منو استفاده کن! 💫",
        reply_markup=get_main_menu()
    )

# ==================== چت با ملورینا ====================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_message.startswith('/'):
        return
    
    not_member = await check_channels(update, context)
    if not_member:
        keyboard = []
        for ch in not_member:
            clean_ch = ch.replace('@', '')
            keyboard.append([InlineKeyboardButton(f"📢 عضویت در {ch}", url=f"https://t.me/{clean_ch}")])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        
        await update.message.reply_text(
            f"🌸 عزیزم! هنوز تو کانال‌ها عضو نشدی! 🥺\n"
            f"برو عضو شو تا باهم حرف بزنیم! 💫",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    history = load_history(user_id)
    history.append(f"کاربر: {user_message}")
    
    reply = get_melorina_response(user_message, history)
    
    history.append(f"ملورینا: {reply}")
    save_history(user_id, history)
    
    await update.message.reply_text(reply, reply_markup=get_chat_buttons())

# ==================== دکمه‌های چت ====================
async def chat_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "ai_idea":
        await query.edit_message_text(
            f"💡 {random.choice(IDEAS)}\n\n🌸 نظرت چیه؟",
            reply_markup=get_chat_buttons()
        )
    elif query.data == "ai_suggest":
        await query.edit_message_text(
            f"💫 {random.choice(SUGGESTS)}\n\n🌸 دوست داری؟",
            reply_markup=get_chat_buttons()
        )
    elif query.data == "ai_joke":
        await query.edit_message_text(
            f"{random.choice(JOKES)}\n\n🌸 خندیدی؟ 😄",
            reply_markup=get_chat_buttons()
        )
    elif query.data == "ai_poem":
        await query.edit_message_text(
            f"{random.choice(POEMS)}\n\n🌸 قشنگ بود؟ 🥰",
            reply_markup=get_chat_buttons()
        )
    elif query.data == "ai_reset":
        save_history(query.from_user.id, [])
        await query.edit_message_text(
            "🔄 ریست شد! از اول شروع می‌کنیم! 🥰\n\n🌸 چی می‌خوای بگی؟",
            reply_markup=get_chat_buttons()
        )
    elif query.data == "chat":
        await query.edit_message_text(
            "💬 **چت با ملورینا** 💬\n\n"
            "🌸 هر چی دوست داری بپرس! من همیشه جواب می‌دم! 🥰\n"
            "📝 جواب‌های من تکراری نیستن!\n\n"
            "فقط پیامت رو بفرست... ✨",
            reply_markup=get_chat_buttons(),
            parse_mode="Markdown"
        )

# ==================== سیستم پرداخت ====================
async def payment_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    formatted = f"{CARD_NUMBER[:4]}-{CARD_NUMBER[4:8]}-{CARD_NUMBER[8:12]}-{CARD_NUMBER[12:]}"
    
    await query.edit_message_text(
        f"💝 **پول توجیبی ملورینا** 💝\n\n"
        f"🌸 اگه دوست داری به من کمک کنی، می‌تونی یه هدیه کوچیک برام بفرستی! 🥰\n\n"
        f"💳 **اطلاعات واریز:**\n"
        f"🏦 شماره کارت: `{formatted}`\n"
        f"👤 صاحب کارت: `{CARD_NAME}`\n\n"
        f"🔒 **امنیت کامل**\n"
        f"• فقط شماره کارت و اسمم رو می‌بینی\n"
        f"• هیچکس نمی‌تونه از کارتم پول برداره\n"
        f"• فقط می‌تونی به کارتم واریز کنی\n\n"
        f"💰 مبلغ رو انتخاب کن:",
        reply_markup=get_payment_menu(),
        parse_mode="Markdown"
    )

async def payment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    amount = query.data.replace("pay_", "")
    
    if amount == "custom":
        await query.edit_message_text(
            "💰 **مبلغ دلخواه رو وارد کن:**\n\n"
            "فقط عدد بفرست (تومان)\n"
            "مثال: 15000\n\n"
            "برای لغو /cancel بفرست.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 برگشت", callback_data="payment")]
            ])
        )
        return WAITING_PAYMENT_AMOUNT
    
    amount = int(amount)
    formatted = f"{CARD_NUMBER[:4]}-{CARD_NUMBER[4:8]}-{CARD_NUMBER[8:12]}-{CARD_NUMBER[12:]}"
    
    await query.edit_message_text(
        f"✅ **مبلغ {amount:,} تومان** انتخاب شد!\n\n"
        f"💳 لطفاً به شماره کارت زیر واریز کن:\n"
        f"`{formatted}`\n\n"
        f"👤 صاحب کارت: `{CARD_NAME}`\n\n"
        f"📸 بعد از واریز، عکس رسید رو برام بفرست.\n"
        f"من تاییدش می‌کنم و اعتبار به حسابت اضافه میشه! 🥰\n\n"
        f"🌸 ممنون از محبتت! 💫",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 برگشت", callback_data="payment")]
        ]),
        parse_mode="Markdown"
    )
    return WAITING_PAYMENT_AMOUNT

async def payment_custom_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "/cancel":
        await update.message.reply_text("❌ لغو شد!", reply_markup=get_main_menu())
        return ConversationHandler.END
    
    try:
        amount = int(text)
        formatted = f"{CARD_NUMBER[:4]}-{CARD_NUMBER[4:8]}-{CARD_NUMBER[8:12]}-{CARD_NUMBER[12:]}"
        
        await update.message.reply_text(
            f"✅ **مبلغ {amount:,} تومان** انتخاب شد!\n\n"
            f"💳 لطفاً به شماره کارت زیر واریز کن:\n"
            f"`{formatted}`\n\n"
            f"👤 صاحب کارت: `{CARD_NAME}`\n\n"
            f"📸 بعد از واریز، عکس رسید رو برام بفرست.\n"
            f"من تاییدش می‌کنم و اعتبار به حسابت اضافه میشه! 🥰\n\n"
            f"🌸 ممنون از محبتت! 💫",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 برگشت", callback_data="payment")]
            ]),
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    except:
        await update.message.reply_text("❌ لطفاً یک عدد معتبر بفرست!")
        return WAITING_PAYMENT_AMOUNT

# ==================== سیستم مانگا ====================
async def manga_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            f"🌸 عزیزم! برای خوندن مانگا باید تو کانال‌ها عضو باشی! 🥺",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    await query.edit_message_text(
        "📖 **بخش مانگا** 📖\n\n"
        "به دنیای مانگا خوش اومدی! 🥰\n\n"
        "🌸 اینجا می‌تونی:\n"
        "• مانگاهای جدید بخونی\n"
        "• مانگا دانلود کنی\n"
        "• مانگا آپلود کنی (ادمین)\n\n"
        "یک گزینه رو انتخاب کن:",
        reply_markup=get_manga_menu()
    )

async def manga_read(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            f"🌸 عزیزم! برای خوندن مانگا باید عضو باشی! 🥺",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    manga_data = load_manga()
    chapters = manga_data.get("chapters", {})
    
    if not chapters:
        await query.edit_message_text(
            "📭 **هیچ مانگایی موجود نیست!** 📭\n\n"
            "🌸 هنوز مانگایی آپلود نشده!\n"
            "به زودی مانگاهای جدید می‌آد! 🥰",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 برگشت", callback_data="manga_menu")]
            ])
        )
        return
    
    keyboard = []
    for num in sorted(chapters.keys(), key=lambda x: int(x)):
        keyboard.append([InlineKeyboardButton(f"📖 فصل {num}", callback_data=f"manga_view_{num}")])
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="manga_menu")])
    
    await query.edit_message_text(
        f"📖 **لیست فصل‌های مانگا** 📖\n\n"
        f"🌸 {len(chapters)} فصل موجود است!\n"
        "یک فصل رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def manga_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            f"🌸 عزیزم! برای خوندن مانگا باید عضو باشی! 🥺",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    chapter_num = query.data.replace("manga_view_", "")
    manga_data = load_manga()
    content = manga_data["chapters"].get(chapter_num, "")
    
    if not content:
        await query.edit_message_text("❌ این فصل موجود نیست!")
        return
    
    keyboard = [
        [InlineKeyboardButton("📥 دانلود متن", callback_data=f"manga_dl_{chapter_num}")],
        [InlineKeyboardButton("🔙 برگشت به لیست", callback_data="manga_read")]
    ]
    
    if len(content) > 4000:
        parts = [content[i:i+4000] for i in range(0, len(content), 4000)]
        for i, part in enumerate(parts):
            await query.message.reply_text(
                f"📖 **فصل {chapter_num} (قسمت {i+1}/{len(parts)})** 📖\n\n{part}",
                parse_mode="Markdown"
            )
        await query.message.reply_text(
            f"🌸 مانگای فصل {chapter_num} تموم شد! 🥰",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(
            f"📖 **فصل {chapter_num}** 📖\n\n{content}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def manga_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chapter_num = query.data.replace("manga_dl_", "")
    manga_data = load_manga()
    content = manga_data["chapters"].get(chapter_num, "")
    
    if not content:
        await query.edit_message_text("❌ این فصل موجود نیست!")
        return
    
    await query.message.reply_document(
        document=content.encode(),
        filename=f"manga_chapter_{chapter_num}.txt",
        caption=f"📖 **فصل {chapter_num} مانگا** 📖\n\n🌸 نوشته شده توسط: ملورینا 🥰"
    )

async def manga_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("⛔ این بخش فقط برای ادمین هست!")
        return
    
    await query.edit_message_text(
        "📤 **آپلود مانگا جدید** 📤\n\n"
        "شماره فصل رو بفرست (مثلاً: ۱):\n\n"
        "برای لغو /cancel بفرست."
    )
    return WAITING_MANGA_NUMBER

async def manga_upload_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "/cancel":
        await update.message.reply_text("❌ لغو شد!", reply_markup=get_main_menu())
        return ConversationHandler.END
    
    try:
        chapter_num = int(text)
        context.user_data['manga_chapter'] = str(chapter_num)
        
        await update.message.reply_text(
            f"✅ شماره فصل {chapter_num} ثبت شد!\n\n"
            "📝 حالا متن مانگا رو بفرست:\n"
            "(می‌تونه طولانی باشه)\n\n"
            "برای لغو /cancel بفرست."
        )
        return WAITING_MANGA_CONTENT
    except:
        await update.message.reply_text("❌ لطفاً یک عدد معتبر بفرست!")
        return WAITING_MANGA_NUMBER
