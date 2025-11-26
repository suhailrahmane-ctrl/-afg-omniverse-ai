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

if st.button("ارسال"):
    if user_input.strip() == "":
        st.warning("لطفاً یک پیام بنویسید!")
    else:
        with st.spinner("در حال دریافت پاسخ از AI..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an intelligent helpful AI assistant."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.1-8b-instant"
            )

            ai_response = chat_completion.choices[0].message["content"]
            st.success("پاسخ AI:")
            st.write(ai_response)
