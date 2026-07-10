import streamlit as st
import replicate
import os
import time
from PIL import Image
import io
import requests

import Replicate from "replicate";
const replicate = new Replicate();

const output = await replicate.run(
  "black-forest-labs/flux-2-pro",
  {
    input: {
      prompt: "Glossy candy-colored 3D letters in hot pink, electric orange, and lime green on a sun-drenched poolside patio with bold terrazzo tiles and vintage lounge chairs in turquoise and yellow. Shot on Kodachrome film with a Hasselblad 500C, warm golden afternoon sunlight, dramatic lens flare, punchy oversaturated colors with that distinctive 70s yellow-orange cast, shallow depth of field with the text sharp in the foreground, tropical palms and a sparkling aquamarine pool behind that spells out \"Run FLUX.2 [pro] on Replicate!\"",
      resolution: "1 MP",
      aspect_ratio: "1:1",
      input_images: [],
      output_format: "webp",
      output_quality: 80,
      safety_tolerance: 2
    }
  }
);
console.log(output);
# Konfigurasi Halaman
st.set_page_config(page_title="MC Production 88 - AI Video", page_icon="🎥", layout="centered")

# Tampilan CSS Profesional
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 50px; background-color: #000; color: white; font-weight: bold; padding: 10px; }
    h1 { color: #333; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 MC Production 88")
st.markdown("<p style='text-align: center;'>Ubah foto produk menjadi video sinematik otomatis.</p>", unsafe_allow_html=True)

def resize_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((768, 768)) 
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

# Antarmuka (Tanpa kolom input API Key)
uploaded_file = st.file_uploader("Upload Foto Produk", type=["jpg", "png", "jpeg"])
prompt = st.text_input("Deskripsi tambahan (Opsional):", "Cinematic product showcase, high quality")

if uploaded_file:
    st.image(uploaded_file, caption="Preview Produk", width=300)
    
    if st.button("Generate Video Sekarang"):
        with st.spinner("AI sedang memproses video... Mohon tunggu sebentar."):
            try:
                # Mengambil kunci secara otomatis dari "Secrets" (Brankas)
                if "REPLICATE_API_TOKEN" in st.secrets:
                    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
                else:
                    st.error("Error: API Token belum diatur di Secrets dashboard!")
                    st.stop()

                resized_img_buffer = resize_image(uploaded_file)
                
                # Menjalankan AI
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457896265005898e3b798e6d24667a4693a9c7b99c0879133481e3a6a978f",
                    input={"input_image": resized_img_buffer, "motion_bucket_id": 10, "fps": 6}
                )
                
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                
                # Fitur Download
                video_bytes = requests.get(video_url).content
                st.download_button("Download Video 📥", data=video_bytes, file_name="mc_production_88.mp4", mime="video/mp4")
                st.success("Video berhasil dibuat!")
                
            except Exception as e:
                st.error(f"Gagal memproses: {e}")

st.markdown("---")
st.caption("© 2026 MC Production 88 | Optimalkan Penjualan dengan AI")
