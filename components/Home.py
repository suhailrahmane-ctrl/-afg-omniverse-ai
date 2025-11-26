import streamlit as st
from components.Navbar import navbar

def home_page():
    navbar()

    st.markdown(
        """
        <h1 style='text-align:center; color:#333;'>Welcome to AFG Genius AI</h1>
        <p style='text-align:center; font-size:18px; color:#555;'>
            نسخه اولیه — سریع، شیک و آماده گسترش!  
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("از منوی بالا صفحات مختلف را باز کن و تست کن.")
