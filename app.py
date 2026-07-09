import streamlit as st
import replicate
import os
import time
from PIL import Image
import io

# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88 - AI Video", page_icon="🎥", layout="centered")

# CSS Kustom
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 MC Production 88 - AI Video Generator")
st.subheader("Ubah Foto Produk Jadi Video Sinematik")

# Fungsi Resize Gambar
def resize_image(image_file):
    img = Image.open(image_file)
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0) # Penting: reset pointer agar bisa dibaca ulang oleh Replicate
    return buf

# Fungsi Utama Generasi Video
def generate_video(image_file, api_key):
    try:
        os.environ["REPLICATE_API_TOKEN"] = api_key
        input_data = {
            "input_image": image_file,
            "motion_bucket_id": 10, 
            "fps": 6
        }
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
            input=input_data
        )
        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar
with st.sidebar:
    st.title("Pengaturan")
    api_key = st.text_input("Replicate API Key", type="password")

# Antarmuka Utama
uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        if not api_key:
            st.error("⚠️ API Key belum dimasukkan!")
        else:
            with st.spinner("AI sedang memproses video... Mohon tunggu."):
                start_time = time.time()
                
                # Gunakan fungsi resize sebelum kirim ke AI
                resized_img_buffer = resize_image(uploaded_file)
                result = generate_video(resized_img_buffer, api_key)
                
                if isinstance(result, str) and result.startswith("Error"):
                    st.error(f"Gagal memproses: {result}")
                else:
                    st.success(f"Video selesai dalam {int(time.time() - start_time)} detik!")
                    st.video(result)
                    
                    # Tombol Download
                    st.download_button(
                        label="Download Video 📥",
                        data=result,
                        file_name="mc_production_88_video.mp4",
                        mime="video/mp4"
                    )
                    st.balloons()

st.markdown("---")
st.markdown("© 2026 MC Production 88 | Optimalkan Penjualan dengan AI")
