import streamlit as st
import pandas as pd


def show_detail_classification(
    selected_data,
    model,
    tfidf
):

    # =====================================
    # Detail Klasifikasi
    # =====================================
    st.divider()

    st.subheader(
        "📄 Detail Klasifikasi"
    )
    st.divider()

    # =====================================
    # Usulan Kamus
    # =====================================
    st.markdown(
        "#### 💡 Usulan Kamus"
    )

    st.info(
        selected_data['Usulan Kamus']
    )

    # =====================================
    # Hasil Preprocessing
    # =====================================
    st.markdown(
        "#### 🔎 Hasil Preprocessing"
    )

    st.code(
        selected_data['clean_text'],
        language='text'
    )

    # =====================================
    # Predict Probability
    # =====================================
    vector = tfidf.transform([
        selected_data['clean_text']
    ])

    probabilities = (
        model.predict_proba(vector)[0]
    )

    labels = model.classes_

    probability_df = pd.DataFrame({

        'OPD': labels,

        'Score': probabilities
    })

    # =====================================
    # Sorting
    # =====================================
    probability_df = (
        probability_df
        .sort_values(
            by='Score',
            ascending=False
        )
    )

    # =====================================
    # Persentase
    # =====================================
    probability_df['Persentase'] = (
        probability_df['Score'] * 100
    ).round(2)

    probability_df['Persentase'] = (
        probability_df['Persentase']
        .astype(str) + '%'
    )

    # =====================================
    # Tabel Probabilitas
    # =====================================
    st.markdown(
        "#### 📊 Tabel Probabilitas OPD"
    )

    st.dataframe(
        probability_df[
            ['OPD', 'Persentase']
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================
    # TOP 2 OPD
    # =====================================
    top2_df = probability_df.head(2)

    # =====================================
    # Hasil Prediksi
    # =====================================
    st.markdown(
        "#### 📈 Hasil Prediksi OPD"
    )

    st.success(
        f"1. {top2_df.iloc[0]['OPD']} "
        f"({top2_df.iloc[0]['Persentase']})"
    )

    st.success(
        f"2. {top2_df.iloc[1]['OPD']} "
        f"({top2_df.iloc[1]['Persentase']})"
    )