# AFG Versatile AI (MVP)

**AFG Versatile AI** — یک اپلیکیشن چندمنظوره هوش مصنوعی (MVP) ساخته‌شده برای موبایل و وب.  
شامل: چت، تولید تصویر، تولید ویدیو (MVP)، تولید صدا، و تولید کد.

## Quick start (mobile-friendly)
1. Deploy to Streamlit:
   - Go to https://share.streamlit.io/
   - New app → Import from GitHub → select this repository → choose `app.py` → Deploy

2. Add API keys (optional, to get full features):
   - Streamlit → Manage app → Settings → Secrets:
     ```
     OPENAI_API_KEY = "your_openai_key"
     REPLICATE_API_TOKEN = "your_replicate_token"
     ELEVEN_API_KEY = "your_elevenlabs_key"
     ```

## Files
- `app.py` — کد اصلی اپ
- `style.css` — استایل
- `requirements.txt` — پکیج‌های لازم

## Notes
- هیچ‌گاه API keys را در این مخزن عمومی قرار نده؛ از Streamlit Secrets استفاده کن.
- برای ارتقا به نسخهٔ حرفه‌ای (Next.js + Tailwind + پایگاه داده و پرداخت) با من ادامه بده.

---

**License:** MIT
