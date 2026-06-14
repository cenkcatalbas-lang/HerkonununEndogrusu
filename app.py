import streamlit as st
import pandas as pd
import json
import os
import re

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# --- FONKSİYONLAR ---
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    
    # 1. Mükerrer sütunları benzersiz yap
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}.{i}" if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols
    
    # 2. Başlıkları temizle (Gereksiz boşlukları ve karakterleri at)
    # Bu işlem sayesinde '06TOLGA0', 'TOLGA ', 'YİĞİT ' gibi değerler 'TOLGA', 'YİĞİT' olur
    new_cols = []
    for col in df.columns:
        clean_col = re.sub(r'[^a-zA-ZçÇğĞıİöÖşŞüÜ0-9]', '', str(col))
        new_cols.append(clean_col)
    df.columns = new_cols
    
    return df

def load_results():
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

# --- ARAYÜZ ---
st.title("🏆 HKED Tahmin Turnuvası")

# Şifre Yönetimi
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if not st.session_state.authenticated:
        if st.text_input("Şifre", type="password") == "1234":
            if st.button("Giriş Yap"):
                st.session_state.authenticated = True
                st.rerun()
    else:
        if st.button("Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()

# --- ANA MANTIK ---
try:
    df = load_data()
    results = load_results()
    
    # Excel'deki bahis oranları sütunları '1', '0', '2' olarak tanımlı varsayıyoruz
    # Katılımcıları 'TARİH', 'TAKIM', 'SAAT', 'GRUP', '1', '0', '2' dışındakiler olarak seç
    exclude_cols = ['TARİH', 'SAAT', 'GRUP', 'MACSONUCU', 'TAKIM1', 'TAKIM2', '1', '0', '2']
    participants = [c for c in df.columns if c not in exclude_cols and not c.startswith('Unnamed')]

    # Admin girişi yapıldıysa sonuç girme ekranı
    if st.session_state.authenticated:
        for idx, row in df.iterrows():
            m_label = f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}"
