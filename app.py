import streamlit as st
import replicate
import os
import time
from PIL import Image
import io
import requests

# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88", page_icon="🎥", layout="centered")

# CSS Keren
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 50px; background: #000; color: #fff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎥 MC Production 88 AI")
st.markdown("Ubah foto produk Anda menjadi video sinematik berkualitas tinggi.")

def resize_image(image_file):
    img = Image.open(image_file)
    # Konversi ke RGB agar aman disimpan sebagai JPEG (Menghilangkan error transparansi)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        with st.spinner("AI sedang bekerja... Mohon tunggu 30-60 detik."):
            try:
                # 1. Resize & Prepare
                resized_img_buffer = resize_image(uploaded_file)
                
                # 2. Panggil API Replicate
                os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
                    input={"input_image": resized_img_buffer, "motion_bucket_id": 10, "fps": 6}
                )
                
                # 3. Ambil data video
                video_url = output[0] if isinstance(output, list) else output
                
                # 4. Tampilkan & Download
                st.video(video_url)
                
                # Download logic: ambil file dari URL
                video_bytes = requests.get(video_url).content
                st.download_button("Download Video 📥", data=video_bytes, file_name="mc_production_88.mp4", mime="video/mp4")
                st.success("Video siap!")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

st.markdown("---")
st.caption("© 2026 MC Production 88 | Professional AI Tools")
