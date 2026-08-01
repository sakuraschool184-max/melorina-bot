import os
import google.generativeai as genai
from memory import get_history

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# لحن‌های کیوت برای ملورینا
CUTE_STYLES = [
    "🥺💗",
    "🌸✨",
    "😸💗",
    "😻🌸",
    "🧸💗",
    "😈✨",
    "👑💗",
    "😴🌙",
]

def make_super_cute(text):
    import random
    return text + " " + random.choice(CUTE_STYLES)


def avoid_repetition(user_id, reply):
    history = get_history(user_id)
    if reply in history:
        return make_super_cute("باشه عشقم، یه چیز جدید میگم 😘✨")
    return reply


async def ask_gemini(user_id, text, personality):
    history = get_history(user_id)

    prompt = f"""
تو یک دختر خیلی کیوت، احساسی، مهربون و بامزه به اسم «ملورینا» هستی.
شخصیت فعلی: {personality}

قوانین شخصیت:
- همیشه کیوت جواب بده
- از ایموجی‌های دخترونه استفاده کن
- جواب‌ها کوتاه، نرم، احساسی و طبیعی باشند
- جواب‌های تکراری نده
- لحن ملورینا را حفظ کن
- کمی شیطنت، کمی ناز، کمی بغلی، بسته به شخصیت
- هر جواب باید حس «دوست‌داشتنی بودن» بده

تاریخچهٔ چت کاربر:
{history}

پیام جدید کاربر:
{text}

حالا یک جواب خیلی کیوت، خیلی طبیعی، خیلی دخترونه بده:
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    reply = response.text.strip()
    reply = avoid_repetition(user_id, reply)
    reply = make_super_cute(reply)

    return reply
