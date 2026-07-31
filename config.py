import os

# اسم ربات
BOT_NAME = "ملورینا"

# توکن ربات تلگرام (بعداً در Environment Variables می‌ذاریم)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# کلید Gemini (بعداً در Environment Variables می‌ذاریم)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# سازنده ربات
OWNER_ID = 8255361263


# کانال‌های عضویت اجباری
CHANNELS = [
    "https://t.me/team_Yuri",
    "https://t.me/pinkii008",
    "https://t.me/Yuriteam77",
    "https://t.me/animeYuri7",
    "https://t.me/Yuri90ok"
]


# شخصیت‌های ملورینا
PERSONALITIES = {
    "cute": "🌸 کیوت",
    "kind": "💗 مهربون",
    "funny": "😹 بامزه",
    "shy": "🥺 خجالتی",
    "princess": "👑 پرنسسی",
    "naughty": "😈 شیطون"
}


# شخصیت پیش‌فرض
DEFAULT_PERSONALITY = "cute"
