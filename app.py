import streamlit as st
import replicate
import os
import time
from PIL import Image
import io

# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88 - AI Video", page_icon="🎥", layout="centered")

# CSS Kustom agar tampilan lebih profesional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 50px; height: 3em; background-color: #000000; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 MC Production 88")
st.subheader("Ubah Foto Produk Jadi Video Sinematik")

# Fungsi Resize Gambar (Agar tidak error karena file terlalu besar)
def resize_image(image_file):
    img = Image.open(image_file)
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

# Fungsi Utama Generasi Video
def generate_video(image_file):
    try:
        # Mengambil API Key dari "Secrets" (Brankas Rahasia Streamlit)
        os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
        
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

# Antarmuka Utama
uploaded_file = st.file_uploader("Upload Foto Produk (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        with st.spinner("AI sedang memproses video... Mohon tunggu 30-60 detik."):
            start_time = time.time()
            
            # Proses resize
            resized_img_buffer = resize_image(uploaded_file)
            
            # Panggil fungsi tanpa perlu kirim API Key lagi (karena sudah diambil otomatis)
            result = generate_video(resized_img_buffer)
            
            if isinstance(result, str) and result.startswith("Error"):
                st.error(f"Gagal memproses: {result}")
            else:
                st.success(f"Berhasil! Dibuat dalam {int(time.time() - start_time)} detik.")
                
                # Menampilkan video
                st.video(result)
                
                # Tombol Download (Otomatis mengambil hasil dari link result)
                st.download_button(
                    label="Download Video 📥",
                    data=result,
                    file_name="mc_production_88_video.mp4",
                    mime="video/mp4"
                )
                st.balloons()

st.markdown("---")
st.markdown("© 2026 MC Production 88 | Optimalkan Penjualan dengan AI")
