import streamlit as st
from components.Home import home_page
from components.ChatBox import chat_box

# تنظیمات صفحه
st.set_page_config(page_title="AFG Genius AI", layout="wide")

# منو برای انتخاب صفحه
menu = ["خانه", "چت‌بات"]
choice = st.sidebar.selectbox("منو", menu)

# نمایش صفحات
if choice == "خانه":
    home_page()
elif choice == "چت‌بات":
    chat_box()
