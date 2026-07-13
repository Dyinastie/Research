import streamlit as st
import pandas as pd
from pathlib import Path
from joblib import load

from preprocessing.preprocessing import preprocess_text

# ============================
# Load Model
# ============================
BASE_DIR = Path(__file__).resolve().parent.parent

model = load(BASE_DIR / "model" / "svm_model.pkl")
tfidf = load(BASE_DIR / "model" / "tfidf_vectorizer.pkl")

# ============================
# Header
# ============================
st.title("🧪 Uji Coba Input")
divider = st.divider()

# ============================
# Input
# ============================
col1, col2 = st.columns([8,2])

with col1:
    usulan = st.text_input(
        "Masukkan satu usulan masyarakat untuk mengetahui OPD yang paling sesuai:",
        placeholder="Contoh: Pengadaan lampu jalan..."
    )

with col2:
    st.write("")
    st.write("")
    prediksi = st.button(
        "Tentukan OPD",
        type="primary",
        use_container_width=True
    )

# ============================
# Prediksi
# ============================
if prediksi:

    if usulan.strip() == "":
        st.warning("Masukkan usulan terlebih dahulu.")
        st.stop()

    # preprocessing
    clean_text = preprocess_text(usulan)

    # tfidf
    vector = tfidf.transform([clean_text])

    # probabilitas
    prob = model.predict_proba(vector)[0]

    classes = model.classes_

    result = (
        pd.DataFrame({
            "OPD": classes,
            "Probabilitas": prob
        })
        .sort_values(
            "Probabilitas",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ============================
    # Hasil OPD
    # ============================
    st.divider()

    st.subheader("📌 Hasil Prediksi")

    c1, c2 = st.columns(2)

    with c1:
        st.success(f"OPD 1\n\n**{result.iloc[0]['OPD']}**")

    with c2:
        st.info(f"OPD 2\n\n**{result.iloc[1]['OPD']}**")

    # ============================
    # Preprocessing
    # ============================
    st.subheader("🧹 Hasil Preprocessing")

    st.code(clean_text)

    # ============================
    # Tabel Probabilitas
    # ============================
    st.subheader("📊 Tabel Probabilitas Setiap OPD")

    result["Probabilitas"] = (
        result["Probabilitas"] * 100
    ).round(2)

    result = result.rename(
        columns={
            "Probabilitas": "Probabilitas (%)"
        }
    )

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )