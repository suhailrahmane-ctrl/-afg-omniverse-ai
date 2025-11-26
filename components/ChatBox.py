import streamlit as st

def chat_box():
    st.header("چت‌بات هوشمند")
    msg = st.chat_input("پیام خود را بنویس...")
    if msg:
        st.chat_message("user").write(msg)
        st.chat_message("assistant").write(f"تو گفتی: '{msg}' — AFG Genius پاسخ داد!")
