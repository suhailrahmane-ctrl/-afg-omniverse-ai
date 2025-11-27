import streamlit as st
import requests

# Load API keys from Streamlit Secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
HF_API_KEY = st.secrets.get("HF_API_KEY", None)

st.title("🌙 AFG Omniverse AI – Chat & Image Generator")

# ---------------- CHATBOT ----------------
st.header("💬 چت‌بات هوشمند")

user_text = st.text_input("پیامت را بنویس:")

if st.button("ارسال"):
    if user_text.strip() == "":
        st.warning("لطفاً متن بنویس!")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_text}]
        }

        response = requests.post(url, json=data, headers=headers)
        bot_answer = response.json()["choices"][0]["message"]["content"]

        st.success(bot_answer)


# ---------------- IMAGE GENERATOR ----------------
st.header("🖼 تولید عکس با HuggingFace")

prompt = st.text_input("توضیح عکس:")

if st.button("تولید عکس"):
    if HF_API_KEY is None:
        st.error("کلید HuggingFace در Secrets پیدا نشد!")
    else:
        hf_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}

        response = requests.post(hf_url, headers=headers, json={"inputs": prompt})

        if response.status_code == 200:
            st.image(response.content)
        else:
            st.error("مشکل در تولید عکس! لطفاً مدل یا کلید را چک کن.")
