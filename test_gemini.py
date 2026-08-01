import os
import google.generativeai as genai

# گرفتن کلید از محیط گیت‌هاب
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ کلید Gemini پیدا نشد! لطفاً در Secrets تنظیم کن.")
    exit(1)

# تنظیم Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# یه تست ساده
try:
    response = model.generate_content("سلام! بگو چطور می‌تونم کمک کنم؟")
    print("✅ پاسخ از Gemini:")
    print(response.text)
except Exception as e:
    print(f"❌ خطا در ارتباط با Gemini: {e}")
