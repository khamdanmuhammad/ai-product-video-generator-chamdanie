import streamlit as st
import replicate
import os
import time

# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88 - AI Video", page_icon="🎥", layout="centered")

# CSS Kustom untuk tampilan lebih bersih
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 MC Production 88 - AI Video Generator")
st.subheader("Ubah Foto Produk Jadi Video Sinematik")

# Sidebar untuk API Key
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=100)
    st.title("Pengaturan")
    api_key = st.text_input("Replicate API Key", type="password", help="Masukkan API Key dari Replicate.com")
    st.info("Pastikan Anda memiliki saldo di akun Replicate agar proses generate berjalan.")

# Fungsi Utama Generasi Video
def generate_video(image_file, api_key):
    try:
        os.environ["REPLICATE_API_TOKEN"] = api_key
        # Menggunakan model Stable Video Diffusion
        input_data = {
            "input_image": image_file,
            "motion_bucket_id": 10, # Nilai 10 cukup aman agar produk tidak "meleleh"
            "fps": 6
        }
        
        # Panggil API
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
            input=input_data
        )
        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Antarmuka Utama
uploaded_file = st.file_uploader("Upload Foto Produk (PNG/JPG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        if not api_key:
            st.error("⚠️ API Key belum dimasukkan! Silakan cek di Sidebar.")
        else:
            with st.spinner("AI sedang memproses video... Mohon tunggu 30-60 detik."):
                start_time = time.time()
                result = generate_video(uploaded_file, api_key)
                
                if isinstance(result, str) and result.startswith("Error"):
                    st.error(f"Gagal memproses: {result}")
                else:
                    st.success(f"Video berhasil dibuat dalam {int(time.time() - start_time)} detik!")
                    st.video(result)
                    st.balloons()
                    st.caption("Hasil karya MC Production 88")

# Footer
st.markdown("---")
st.markdown("© 2026 MC Production 88 | Optimalkan Penjualan dengan AI")
