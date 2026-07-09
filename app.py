import streamlit as st
import replicate
import os
import time
from PIL import Image
import io
import requests

st.set_page_config(page_title="MC Production 88 AI", page_icon="🎥")

# CSS Keren
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 50px; background: #000; color: #fff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎥 MC Production 88 AI")
st.markdown("Ubah foto produk jadi video sinematik dengan instruksi khusus.")

def resize_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

# Input User
uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "png", "jpeg"])
user_prompt = st.text_input("Ingin video seperti apa? (Contoh: Smooth zoom in, Cinematic lighting, slow motion)", 
                            "Professional product showcase, cinematic lighting, smooth movement")

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        with st.spinner("AI sedang memproses..."):
            try:
                # Setup API
                api_token = st.secrets["REPLICATE_API_TOKEN"]
                os.environ["REPLICATE_API_TOKEN"] = api_token
                
                resized_img_buffer = resize_image(uploaded_file)
                
                # Menggunakan Model SVD (Stable Video Diffusion)
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
                    input={
                        "input_image": resized_img_buffer, 
                        "motion_bucket_id": 10, 
                        "fps": 6
                    }
                )
                
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                
                # Download
                video_bytes = requests.get(video_url).content
                st.download_button("Download Video 📥", data=video_bytes, file_name="mc_production_88.mp4", mime="video/mp4")
                
            except Exception as e:
                st.error(f"Error: {e}. Pastikan API Key di Secrets sudah benar.")

st.markdown("---")
st.caption("© 2026 MC Production 88")
