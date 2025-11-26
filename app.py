# app.py
import streamlit as st
import requests
from io import BytesIO
from gtts import gTTS
from PIL import Image
import base64
import time
import os

# Optional imports (if available)
try:
    import replicate
except Exception:
    replicate = None

try:
    import openai
except Exception:
    openai = None

# moviepy for simple local slideshow->video (optional)
try:
    from moviepy.editor import ImageClip, concatenate_videoclips
except Exception:
    ImageClip = None

# Page config and load css
st.set_page_config(page_title="AFG Versatile AI", layout="wide", initial_sidebar_state="expanded")
if os.path.exists("style.css"):
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helpers
def encode_audio_bytes(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    return f"data:audio/mp3;base64,{b64}"

def chat_respond(prompt, history=None):
    """Use OpenAI if key present, otherwise fallback echo."""
    if "OPENAI_API_KEY" in st.secrets and openai is not None:
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini" if hasattr(openai, "ChatCompletion") else "gpt-4o-mini",
                messages=[{"role":"system","content":"You are a helpful assistant."}] + (
                    [{"role":"user","content":h} for h in (history or [])] + [{"role":"user","content":prompt}]
                ),
                max_tokens=600,
                temperature=0.2
            )
            text = resp["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            return f"(OpenAI error — fallback) پاسخ محلی: {prompt}\n\nخطا: {e}"
    # fallback simple reply
    return f"پاسخ آزمایشی: من دیدم: «{prompt}». اگر کلید OpenAI را اضافه کنی پاسخ بهتری می‌گیرى."

def generate_image(prompt):
    """Try Replicate (if token present), otherwise create placeholder image."""
    if "REPLICATE_API_TOKEN" in st.secrets and replicate is not None:
        try:
            client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])
            model = "stability-ai/stable-diffusion-xl-beta-1-0"
            output = client.run(model, input={"prompt": prompt})
            if isinstance(output, list):
                return output[0]
            return output
        except Exception as e:
            st.error(f"Replicate error: {e}")
            return None
    # Fallback: placeholder image with prompt text
    img = Image.new("RGB", (1024, 640), color=(245,245,247))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(img)
    text = "Placeholder\n\n" + (prompt[:200])
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = None
    d.multiline_text((40,40), text, fill=(16,16,20), font=font)
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio

def tts_generate(text, voice="alloy"):
    """Try ElevenLabs if key present, else use gTTS fallback."""
    if "ELEVEN_API_KEY" in st.secrets:
        try:
            API_KEY = st.secrets["ELEVEN_API_KEY"]
            url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice
            headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
            payload = {"text": text, "voice": voice}
            r = requests.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                return BytesIO(r.content)
            else:
                st.error(f"ElevenLabs error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"ElevenLabs exception: {e}")
    # fallback gTTS
    try:
        tts = gTTS(text, lang="fa")
        bio = BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        return bio
    except Exception as e:
        st.error(f"gTTS error: {e}")
        return None

def make_video_from_images(image_bytes_list, fps=1, duration_per_image=2, out_name="out.mp4"):
    if ImageClip is None:
        st.error("moviepy نصب نیست. برای ساخت ویدیو محلی moviepy لازم است.")
        return None
    clips = []
    for b in image_bytes_list:
        if isinstance(b, BytesIO):
            b.seek(0)
            img = Image.open(b).convert("RGB")
            clip = ImageClip(img).set_duration(duration_per_image)
            clips.append(clip)
        elif isinstance(b, str) and b.startswith("http"):
            try:
                r = requests.get(b)
                bio = BytesIO(r.content)
                img = Image.open(bio).convert("RGB")
                clip = ImageClip(img).set_duration(duration_per_image)
                clips.append(clip)
            except:
                pass
    if not clips:
        st.error("هیچ فریمی برای ویدیو وجود ندارد.")
        return None
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(out_name, fps=fps, codec="libx264", audio=False, verbose=False, logger=None)
    return out_name

# UI
st.markdown("<div style='padding:18px 0;'><h2 style='margin:0'>AFG Versatile AI — MVP</h2><div style='color:#666;'>چت • تصویر • ویدیو • صدا • کدنویسی</div></div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("راهنمای راه‌اندازی")
    st.write("برای کلیدها: Streamlit → Manage app → Settings → Secrets")
    st.write("- OPENAI_API_KEY: برای چت و تولید کد")
    st.write("- REPLICATE_API_TOKEN: برای تولید تصویر")
    st.write("- ELEVEN_API_KEY: برای صدای طبیعی (اختیاری)")
    st.markdown("---")
    st.write("وضعیت کلیدها:")
    for k in ("OPENAI_API_KEY","REPLICATE_API_TOKEN","ELEVEN_API_KEY"):
        st.write(k, "✅" if k in st.secrets else "❌")

if "messages" not in st.session_state:
    st.session_state.messages = []

tabs = st.tabs(["چت‌بات", "تولید عکس", "تولید ویدیو (MVP)", "تولید صدا", "کدنویسی"])

with tabs[0]:
    st.header("چت‌بات هوشمند")
    user_input = st.chat_input("اینجا بنویس ...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("در حال فکر کردن..."):
            history_texts = [m["content"] for m in st.session_state.messages if m["role"]=="user"]
            reply = chat_respond(user_input, history=history_texts)
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.chat_message("assistant").write(reply)
    if st.button("پاک کردن حافظه"):
        st.session_state.messages = []
        st.experimental_rerun()

with tabs[1]:
    st.header("تولید تصویر")
    prompt_img = st.text_area("توضیح تصویر (prompt)", placeholder="مثال: مناظر کوهستانی با نور غروب")
    if st.button("تولید تصویر"):
        if not prompt_img:
            st.warning("لطفاً یک توضیح وارد کن")
        else:
            with st.spinner("در حال تولید تصویر ..."):
                out = generate_image(prompt_img)
                if isinstance(out, BytesIO):
                    st.image(out, use_column_width=True)
                    st.download_button("دانلود PNG", out, file_name="afg_image.png")
                elif isinstance(out, str) and out.startswith("http"):
                    st.image(out, use_column_width=True)
                    st.markdown(f"[باز کردن در تب جدید]({out})")
                else:
                    st.write("خروجی نامعلوم:", out)

with tabs[2]:
    st.header("تولید ویدیو (MVP)")
    st.info("چند خط متن بنویس؛ هر خط → یک فریم تصویر.")
    prompts = st.text_area("هر خط یک فریم:", height=140)
    if st.button("ساخت ویدیو"):
        lines = [l.strip() for l in prompts.splitlines() if l.strip()]
        if not lines:
            st.warning("لطفاً چند خط وارد کن")
        else:
            imgs = []
            for ln in lines:
                out = generate_image(ln)
                if isinstance(out, BytesIO):
                    imgs.append(out)
                elif isinstance(out, str) and out.startswith("http"):
                    try:
                        r = requests.get(out)
                        imgs.append(BytesIO(r.content))
                    except:
                        pass
            if not imgs:
                st.error("هیچ تصویری ساخته نشد.")
            else:
                if ImageClip is None:
                    st.warning("moviepy نصب نیست؛ تصاویر را نمایش می‌کنم.")
                    for i,b in enumerate(imgs):
                        st.image(b, caption=f"فریم {i+1}", use_column_width=True)
                else:
                    st.info("در حال ساخت ویدیو ...")
                    outfile = f"afg_vid_{int(time.time())}.mp4"
                    res = make_video_from_images(imgs, duration_per_image=2, out_name=outfile)
                    if res:
                        with open(res,"rb") as f:
                            st.video(f.read())

with tabs[3]:
    st.header("تولید صدا (TTS)")
    text_tts = st.text_area("متن برای تبدیل به صدا", height=120)
    voice_choice = st.selectbox("انتخاب صدا (اگر موجود)", ["alloy","default"])
    if st.button("ساخت صدا"):
        if not text_tts:
            st.warning("متن وارد نشده")
        else:
            with st.spinner("در حال ساخت صدا ..."):
                audio_bio = tts_generate(text_tts, voice=voice_choice)
                if audio_bio:
                    st.audio(audio_bio.getvalue())
                    st.download_button("دانلود MP3", audio_bio, file_name="afg_voice.mp3")

with tabs[4]:
    st.header("کدنویسی / تولید کد")
    code_prompt = st.text_area("چی می‌خوای کدش بسازه؟", height=140)
    if st.button("تولید کد"):
        if not code_prompt:
            st.warning("لطفاً یک توضیح بده")
        else:
            if "OPENAI_API_KEY" in st.secrets and openai is not None:
                try:
                    openai.api_key = st.secrets["OPENAI_API_KEY"]
                    resp = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=f"Write code for: {code_prompt}\nInclude comments and example usage.",
                        max_tokens=600,
                        temperature=0.1,
                    )
                    code_text = resp["choices"][0]["text"]
                    st.code(code_text, language="python")
                    st.download_button("دانلود کد .py", code_text, file_name="afg_code.py")
                except Exception as e:
                    st.error(f"OpenAI error: {e}")
            else:
                sample = "# نمونهٔ آفلاین (fallback)\n\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(n-1):\n        a, b = b, a+b\n    return b\n\nprint(fibonacci(10))\n"
                st.info("OpenAI متصل نیست — کد نمونه آفلاین نمایش داده می‌شود.")
                st.code(sample, language="python")
                st.download_button("دانلود کد نمونه", sample, file_name="afg_code_sample.py")

st.markdown("<div style='margin-top:18px;color:#666;font-size:14px;'>AFG Versatile AI • MVP — ساخته شده برای موبایل و وب — سهیل جان</div>", unsafe_allow_html=True)
