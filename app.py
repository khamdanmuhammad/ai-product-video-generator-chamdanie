import streamlit as st
import replicate
import os
import io
import requests
from PIL import Image

# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88", page_icon="🎥", layout="centered")

# CSS Kustom
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 50px; background-color: #000; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 MC Production 88")
st.markdown("<p style='text-align: center;'>Ubah foto produk menjadi video sinematik.</p>", unsafe_allow_html=True)

# Fungsi Resize
def resize_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

# Antarmuka
uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        with st.spinner("AI sedang memproses... Mohon tunggu."):
            try:
                # Mengambil API Token dari Secrets
                os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
                
                resized_img_buffer = resize_image(uploaded_file)
                
                # Menjalankan model
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
                    input={"input_image": resized_img_buffer, "motion_bucket_id": 10, "fps": 6}
                )
                
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                
                # Tombol Download
                video_bytes = requests.get(video_url).content
                st.download_button("Download Video 📥", data=video_bytes, file_name="mc_production_88.mp4", mime="video/mp4")
                st.success("Video berhasil dibuat!")
                
            except Exception as e:
                st.error(f"Gagal memproses: {e}")

st.markdown("---")
st.caption("© 2026 MC Production 88")
