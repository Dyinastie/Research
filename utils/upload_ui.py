import streamlit as st


def upload_ui():

    st.markdown("""
    <style>

    /* Hilangkan drag drop */
    [data-testid="stFileUploaderDropzone"]{
        border: none;
        background: transparent;
        padding: 0;
    }

    /* Hilangkan teks instruksi */
    [data-testid="stFileUploaderDropzoneInstructions"]{
        display: none;
    }

    /* Sembunyikan file uploaded */
    [data-testid="stFileUploader"] ul{
        display: none;
    }

    /* Tombol upload */
    [data-testid="stBaseButton-secondary"]{
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Hover */
    [data-testid="stBaseButton-secondary"]:hover{
        background-color: #1D4ED8 !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)