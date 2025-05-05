import streamlit as st  # type: ignore
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt  # type: ignore
import altair as alt
import plotly.express as px  # type: ignore
from PIL import Image  # type: ignore
from PyPDF2 import PdfReader  # type: ignore

# =========================
# Konfigurasi Halaman
# =========================
st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

# =========================
# Judul dan Pengantar
# =========================
st.title("Aplikasi Dasar dengan Streamlit")
st.subheader("Aplikasi pertama Streamlit")
st.caption("Data ini hanya untuk tujuan demonstrasi.")

# =========================
# Menampilkan DataFrame Sederhana
# =========================
data = {
    'Nama': ['ahmad', 'fairuz', 'dabbir', 'nura', 'aco'],
    'Usia': [20, 25, 30, 17, 35],
    'Kota': ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Malang']
}
df = pd.DataFrame(data)
st.write("### Tabel Data Pengguna:")
st.dataframe(df)

# =========================
# Mengambil Data dari API
# =========================
st.write("### Data dari API (jsonplaceholder.typicode.com)")

@st.cache_data
def load_api_data():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Gagal mengambil data dari API: {e}")
        return pd.DataFrame()

api_df = load_api_data()
if not api_df.empty:
    st.dataframe(api_df)

# =========================
# Upload File CSV
# =========================
st.write("### Upload File CSV")
uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
if uploaded_file is not None:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        st.write("Data dari file yang diunggah:")
        st.dataframe(uploaded_df)
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
else:
    st.info("Silakan unggah file untuk melihat datanya.")

# =========================
# Menampilkan DataFrame Acak (perbaikan duplikat kolom)
# =========================
columns = [f"col_{i}" for i in range(5)]
random_df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=columns
)
st.write("### DataFrame Random:")
st.dataframe(random_df)

# =========================
# Menampilkan Metrik
# =========================
st.write("### Statistik Utama")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Omset", value="Rp 200 Juta", delta="+5%")
with col2:
    st.metric(label="User Aktif", value="1.250", delta="+2%")
with col3:
    st.metric(label="Refund", value="15", delta="-1%")

# =========================
# Line Chart Streamlit
# =========================
st.write("### Line Chart (Streamlit)")
line_data = pd.DataFrame(
    np.random.randn(100, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(line_data)

# =========================
# Grafik Altair
# =========================
st.write("### Grafik Altair")
alt_chart = alt.Chart(line_data.reset_index()).mark_line().encode(
    x='index',
    y='a'
)
st.altair_chart(alt_chart, use_container_width=True)

# =========================
# Grafik Plotly
# =========================
st.write("### Grafik Penjualan dan Laba (Plotly)")
sales_data = pd.DataFrame({
    'Tahun': [2018, 2019, 2020, 2021, 2022],
    'Penjualan': [100, 120, 90, 140, 180],
    'Laba': [20, 30, 15, 35, 50]
})

fig_penjualan = px.line(
    sales_data,
    x='Tahun',
    y='Penjualan',
    markers=True,
    title='✅ Tren Penjualan Tiap Tahun',
    labels={'Penjualan': 'Jumlah Penjualan', 'Tahun': 'Tahun'},
    template='plotly_white'
)
fig_penjualan.update_layout(title_x=0.5)

fig_laba = px.bar(
    sales_data,
    x='Tahun',
    y='Laba',
    color='Tahun',
    title='💵 Laba Tahunan',
    labels={'Laba': 'Jumlah Laba'},
    template='plotly_dark'
)
fig_laba.update_layout(title_x=0.5)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_penjualan, use_container_width=True)
with col2:
    st.plotly_chart(fig_laba, use_container_width=True)

# =========================
# Menampilkan Gambar
# =========================
st.write("### Gambar dari File dan URL")
try:
    image = Image.open('flask-horizontal.webp')
    st.image(image, caption="Gambar dari file lokal")
except FileNotFoundError:
    st.warning("Gambar lokal tidak ditemukan: flask-horizontal.webp")

st.image(
    'https://cdn.sulselsatu.com/imageresize/assets/media/upload/2025/04/WhatsApp-Image-2025-04-27-at-16.25.16.jpeg&width=200&height=112',
    caption="Gambar dari URL",
    use_column_width=True
)

# =========================
# Video dan Audio
# =========================
st.write("### Video dan Audio")
try:
    st.video('video.mp4')
except Exception:
    st.warning("File video.mp4 tidak ditemukan atau tidak dapat diputar.")

try:
    st.audio('audio.mp3')
except Exception:
    st.warning("File audio.mp3 tidak ditemukan atau tidak dapat diputar.")

# =========================
# Menampilkan Isi File PDF
# =========================
st.write("### Pembaca PDF")
uploaded_pdf = st.file_uploader("Pilih file PDF", type=["pdf"])
if uploaded_pdf is not None:
    try:
        reader = PdfReader(uploaded_pdf)
        pdf_text = "".join(page.extract_text() or '' for page in reader.pages)
        st.text_area("Isi PDF:", pdf_text, height=300)
    except Exception as e:
        st.error(f"Gagal membaca PDF: {e}")

# =========================
# Navigasi Sidebar
# =========================
st.sidebar.header("Navigasi")
selection = st.sidebar.radio("Pilih Halaman", ["Beranda", "Tentang", "Kontak"])
if selection == "Beranda":
    st.write("## Beranda")
    st.write("Ini adalah halaman beranda.")
elif selection == "Tentang":
    st.write("## Tentang")
    st.write("Ini adalah halaman tentang aplikasi ini.")
else:
    st.write("## Kontak")
    st.write("Silakan hubungi kami di email@example.com")
