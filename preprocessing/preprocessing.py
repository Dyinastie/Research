import re
import pandas as pd
import nltk
from pathlib import Path
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# =====================================
# Load Kamus Normalisasi
# =====================================
BASE_DIR = Path(__file__).resolve().parent

norm_df = pd.read_csv(
    BASE_DIR / "Kamus Normalisasi.csv",
    sep=";"
)

normalization_dict = {
    row['Singkatan']: row['Kata Lain'] for _, row in norm_df.iterrows()
}

# =====================================
# Inisialisasi NLP
# =====================================
tokenizer = WordPunctTokenizer()

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
stop_words = set(stopwords.words('indonesian'))

factory = StemmerFactory()
stemmer = factory.create_stemmer()

# =====================================
# Fungsi Preprocessing
# =====================================
def preprocess_text(text):

    # Handle data kosong
    if pd.isna(text):
        return ""

    # Ubah ke string
    text = str(text)

    # lowercase
    text = text.lower()

    # hapus simbol tertentu
    text = re.sub(r'[/\-]', ' ', text)

    # hapus tanda baca
    text = re.sub(r'[^\w\s]', '', text)

    # hapus angka
    text = re.sub(r'\d+', '', text)

    # hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    # tokenisasi
    tokens = tokenizer.tokenize(text)

    # hapus token pendek
    tokens = [word for word in tokens if len(word) > 1]

    # normalisasi
    normalized = []

    for word in tokens:
        norm_word = normalization_dict.get(word, word) 
        normalized.extend(norm_word.split())

    # stopword removal
    tokens = [
        word for word in normalized if word not in stop_words
    ]

    # stemming
    tokens = [
        stemmer.stem(word) for word in tokens
    ]

    return " ".join(tokens)