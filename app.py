import streamlit as st
from groq import Groq

st.set_page_config(page_title="AFG Genius AI", page_icon="🤖", layout="wide")

# Load API key
import os
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

st.title("🤖 AFG Genius - چت‌بات هوشمند")
st.write("سهیل جان، پیام خود را بنویسید👇")

# Chat UI
user_input = st.text_input("پیام شما:")

# --- داخل بلوک ارسال پیام (جایگزین بلوک قبلی) ---
if st.button("ارسال"):
    if user_input.strip() == "":
        st.warning("لطفاً یک پیام بنویسید!")
    else:
        with st.spinner("در حال دریافت پاسخ از AI..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an intelligent helpful AI assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    model="llama-3.1-8b-instant"
                )
            except Exception as e:
                st.error("خطا هنگام تماس با سرویس Groq:\n" + str(e))
                # برای دیباگ بیشتر می‌توانیم لاگ کامل را بنویسیم:
                st.write("جزئیات خطا را در لاگ‌ها چک کن.")
                raise

            # استخراج امن پاسخ از ساختارهای ممکن
            ai_response = None
            try:
                # حالت دیکشنری‌مانند
                if isinstance(chat_completion, dict):
                    ai_response = (chat_completion.get("choices", [{}])[0]
                                           .get("message", {})
                                           .get("content"))
                # حالت شیء با صفات
                if not ai_response:
                    # try .choices[0].message.content
                    choices = getattr(chat_completion, "choices", None)
                    if choices:
                        first = choices[0]
                        # message might be attribute or dict
                        msg = getattr(first, "message", None) or (first.get("message") if isinstance(first, dict) else None)
                        if msg:
                            ai_response = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
                # fallback: try common dict access
                if not ai_response:
                    try:
                        ai_response = chat_completion["choices"][0]["message"]["content"]
                    except Exception:
                        pass
                # نهایی: اگر هنوز خالی است، تبدیل به رشته
                if not ai_response:
                    ai_response = str(chat_completion)
            except Exception as ex:
                ai_response = f"(خطا در پردازش پاسخ): {ex}\nخام: {str(chat_completion)}"

            # نمایش پاسخ
            st.success("پاسخ AI:")
            st.write(ai_response)
