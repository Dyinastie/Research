import streamlit as st

st.set_page_config(
    page_title="Klasifikasi OPD",
    layout="wide"
)

st.title("🏠 Beranda")

st.divider()

st.subheader("📘 Panduan Penggunaan")

st.markdown("""
#### Cara Menggunakan Aplikasi
1. Masuk ke menu **Klasifikasi**.
2. Klik **Upload** dan pilih seluruh file Excel Identifikasi Permasalahan per kelurahan.
3. Sistem akan otomatis melakukan proses:
   - Preprocessing teks
   - TF-IDF
   - Klasifikasi SVM
   - Menampilkan hasil klasifikasi OPD dalam bentuk tabel
4. Unduh hasil klasifikasi melalui tombol **Export File**.
""")

st.divider()

st.subheader("📄 Ketentuan File Excel Identifikasi Permasalahan")

# Ketentuan 1
st.markdown("""
#### 1. Format Nama File

Nama file wajib menggunakan format:

**Kecamatan - Kelurahan.xlsx**

Contoh:
- Blimbing - Arjosari.xlsx
- Klojen - Samaan.xlsx
""")

st.image(
    "assets/contoh_nama_file.png",
    caption="Contoh format penamaan file",
    width=200,
)

# Ketentuan 2
st.markdown("""
#### 2. Struktur Kolom

Pastikan file Excel mengikuti template yang telah disediakan oleh Bappeda Kota Malang dan memuat kolom berikut:

- Arah Kebijakan Pembangunan Kota Malang
- No.
- Permasalahan
- Penyebab
- Lokasi
- Usulan Kamus
- Keterangan
""")

st.image(
    "assets/contoh_template.png",
    caption="Contoh struktur file Excel",
    use_container_width=True
)

# Ketentuan 3
st.markdown("""
#### 3. File Tanpa Data Usulan

Apabila tidak terdapat data usulan pada suatu kelurahan:

- Tetap gunakan format file yang sesuai.
- Jangan menghapus struktur tabel.
- Kosongkan kolom mulai dari **No.** hingga **Keterangan**.
""")

st.image(
    "assets/contoh_file_kosong.png",
    caption="Contoh file tanpa data usulan",
    use_container_width=True
)

# Contoh Penulisan File Yang Benar
st.markdown("""
#### Contoh Penulisan File Yang Benar
""")

st.image(
    "assets/contoh_file_benar.png",
    caption="Contoh Penulisan File Yang Benar",
    use_container_width=True
)

# Contoh Penulisan File Yang Salah
st.markdown("""
#### Contoh Penulisan File Yang Salah

File dianggap salah jika:

- Terdapat nama kolom yang diubah atau dihapus.
- Terdapat modifikasi pada struktur tabel, seperti melakukan "merge cell" atau menambahkan kolom baru.
""")

st.image(
    "assets/contoh_file_salah.png",
    caption="Contoh Penulisan File Yang Salah",
    use_container_width=True
)