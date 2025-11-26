import streamlit as st
from components.Home import home_page
from components.ChatBox import chat_box

st.set_page_config(page_title="AFG Genius AI", layout="wide")

# تب‌ها
tabs = ["خانه", "چت‌بات", "تولید عکس", "تولید ویدیو", "تولید صدا", "کدنویسی", "ترجمه"]
tab_choice = st.sidebar.radio("منو", tabs)

if tab_choice == "خانه":
    home_page()
elif tab_choice == "چت‌بات":
    chat_box()
elif tab_choice == "تولید عکس":
    st.header("تولید عکس")
    st.info("به زودی با مدل FLUX.1 🔥")
elif tab_choice == "تولید ویدیو":
    st.header("تولید ویدیو")
    st.info("به زودی با مدل Wan 2.2 🔥")
elif tab_choice == "تولید صدا":
    st.header("تولید صدا")
    st.info("به زودی با Google TTS یا ElevenLabs 🔥")
elif tab_choice == "کدنویسی":
    st.header("کدنویسی / برنامه نویسی")
    st.info("به زودی با Code Llama یا GPT-5 🔥")
elif tab_choice == "ترجمه":
    st.header("ترجمه زنده")
    st.info("به زودی با Google Translate API 🔥")
