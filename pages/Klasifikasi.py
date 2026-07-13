import streamlit as st
import pandas as pd
from pathlib import Path
from utils.upload_ui import (upload_ui)
from joblib import load
from utils.prediction import (predict_top_opd)
from utils.export import (export_excel)
from utils.detail_classification import (show_detail_classification)
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from preprocessing.preprocessing import preprocess_text

# =====================================
# Load Model & TF-IDF
# =====================================
BASE_DIR = Path(__file__).resolve().parent.parent

model = load(BASE_DIR / "model" / "svm_model.pkl")
tfidf = load(BASE_DIR / "model" / "tfidf_vectorizer.pkl")

# =====================================
# Header
# =====================================
st.title("📊 Klasifikasi Usulan Masyarakat")

st.divider()

# =====================================
# Upload
# =====================================
upload_ui()
col1, col2 = st.columns([7, 1])

with col2:
    uploaded_files = st.file_uploader(
    "Upload Excel",
    type=["xlsx"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# =====================================
# Jika Upload
# =====================================
if uploaded_files:

    try:

        # =====================================
        # Read Excel
        # =====================================
        arah_kebijakan_master = None
        all_data = []
        empty_files = set()

        for file in uploaded_files:

            # Baca tanpa header terlebih dahulu
            raw_df = pd.read_excel(file, header=None)

            # Cari baris yang mengandung "No."
            header_row = raw_df[
                raw_df.apply(
                    lambda x: x.astype(str)
                            .str.strip()
                            .eq("No.")
                            .any(),
                    axis=1
                )
            ].index

            # Jika tidak ditemukan baris header, anggap file kosong
            if len(header_row) == 0:
                empty_files.add(file.name)
                continue

            df = pd.read_excel(
                file,
                header=header_row[0]
            )

            # Rapikan nama kolom
            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
            )

            # Rename Kolom Merge
            df = df.rename(columns={
                df.columns[0]: "Arah_Kebijakan_No",
                df.columns[1]: "Arah_Kebijakan_Deskripsi"
            })

            # Simpan Arah Kebijakan 
            if arah_kebijakan_master is None:

                arah_filter = df[
                    df[
                        "Arah_Kebijakan_No"
                    ]
                    .astype(str)
                    .str.contains(
                        r'\d',
                        na=False
                    )
                ]

                arah_kebijakan_master = (
                    arah_filter[
                        "Arah_Kebijakan_Deskripsi"
                    ]
                    .reset_index(drop=True)
                )

            # Hapus baris kosong
            df = df.dropna(how="all")

            # Cek jika file kosong
            if "No." not in df.columns:
                empty_files.add(file.name)
                continue

            if df["No."].dropna().astype(str).str.strip().eq("").all():
                empty_files.add(file.name)
                continue

            # Filter data yang memiliki nomor urut
            df = df[
                df['No.']
                .astype(str)
                .str.contains(
                    r'\d',
                    na=False
                )
            ]

            # Tambahkan nama file
            df["source_file"] = file.name

            # Ambil Kecamatan & Kelurahan
            file_name = (
                file.name
                .replace(".xlsx", "")
            )
            split_name = file_name.split("-", 1)
            if len(split_name) < 2:
                st.error(
                    f"Format nama file tidak sesuai: {file.name}"
                )
                continue
            kecamatan = split_name[0].strip()
            kelurahan = split_name[1].strip()
            df["Kecamatan"] = kecamatan
            df["Kelurahan"] = kelurahan

            all_data.append(df)

        # Gabungkan semua file
        if len(all_data) == 0:
            st.error("❌ Semua file kosong atau tidak memiliki data usulan.")
            st.stop()

        df = pd.concat(
            all_data,
            ignore_index=True
        )

        # Isi Arah Kebijakan 1 Saja
        df[
            "Arah_Kebijakan_Export"
        ] = arah_kebijakan_master.reindex(
            df.index
        )

        # Mapping Kode Kecamatan
        df["Kecamatan"] = df["Kecamatan"].str.strip()
        mapping = {
            "Blimbing": "BL",
            "Klojen": "KL",
            "Kedungkandang": "KD",
            "Lowokwaru": "LW",
            "Sukun": "SK"
        }
        df["KodePrefix"] = df["Kecamatan"].map(mapping)
        if df["KodePrefix"].isna().any():
            st.error("Terdapat nama kecamatan yang tidak sesuai format.")
            st.stop()        
        df["NoUrut"] = df.groupby("Kecamatan").cumcount() + 1
        df["Kode"] = df["KodePrefix"] + "." + df["NoUrut"].astype(str).str.zfill(2)
        df = df.drop(columns=["KodePrefix", "NoUrut"])

        # =====================================
        # Required Columns
        # =====================================
        required_columns = [
            'No.',
            'Permasalahan',
            'Penyebab',
            'Lokasi',
            'Usulan Kamus'
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        # =====================================
        # Validasi Kolom
        # =====================================
        if missing_columns:

            st.error(
                f"Kolom tidak ditemukan: "
                f"{', '.join(missing_columns)}"
            )

        else:

            # =====================================
            # Preprocessing & Prediksi
            # =====================================
            with st.spinner(
                "Melakukan klasifikasi OPD..."
            ):

                df['clean_text'] = (
                    df['Usulan Kamus']
                    .astype(str)
                    .apply(preprocess_text)
                )

                vector = tfidf.transform(
                    df['clean_text']
                )

                top1, top2 = predict_top_opd(
                    model,
                    vector
                )

                df['OPD_1'] = top1
                df['OPD_2'] = top2

            # =====================================
            # Kolom Tampil
            # =====================================
            display_columns = [
                'No.',
                'Kecamatan',
                'Kelurahan',
                'Permasalahan',
                'Penyebab',
                'Lokasi',
                'Usulan Kamus',
                'OPD_1',
                'OPD_2',
                'clean_text'
            ]

            display_df = df.copy()
            display_df = display_df[display_columns]

            # =====================================
            # Tabel Interaktif
            # =====================================
            st.subheader(
                "📋 Hasil Klasifikasi"
            )

            gb = GridOptionsBuilder.from_dataframe(
                display_df
            )

            gb.configure_selection(
                selection_mode="single",
                use_checkbox=False
            )

            gb.configure_column("clean_text", hide=True)

            gb.configure_pagination(
                paginationAutoPageSize=False,
                paginationPageSize=10
            )

            gb.configure_default_column(
                sortable=True,
                filter=True,
                resizable=True,
                wrapText=True,
                autoHeight=True
            )

            grid_options = gb.build()

            grid_response = AgGrid(
                display_df,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=450,
                theme="balham"
            )

            # =====================================
            # Warning file kosong
            # =====================================
            if empty_files:
                st.warning("⚠️ Terdapat file yang tidak memiliki data usulan:")

                for f in empty_files:
                    st.write(f"- {f}")

            # =====================================
            # Export Excel
            # =====================================
            output = export_excel(df)

            col_left, col_right = st.columns([7, 1])

            with col_right:

                st.download_button(
                    label="Download Hasil",
                    data=output,
                    file_name="Form Identifikasi Isi.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                    ),
                    use_container_width=True
                )

            # =====================================
            # Detail Klasifikasi
            # =====================================
            selected_rows = grid_response.get(
                "selected_rows",
                []
            )

            selected_data = None

            if (
                isinstance(
                    selected_rows,
                    pd.DataFrame
                )
                and
                not selected_rows.empty
            ):

                selected_data = (
                    selected_rows.iloc[0]
                )

            elif (
                isinstance(
                    selected_rows,
                    list
                )
                and
                len(selected_rows) > 0
            ):

                selected_data = (
                    selected_rows[0]
                )

            if selected_data is not None:

                show_detail_classification(
                    selected_data,
                    model,
                    tfidf
                )

    except Exception as e:

        st.error(
            f"Terjadi kesalahan: {e}"
        )

# =====================================
# Belum Upload
# =====================================
else:

    st.info(
        "Silakan import file Excel terlebih dahulu."
    )