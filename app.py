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
    # Mükerrer sütunları benzersiz yap
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}.{i}" if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols
    
    # Başlıkları temizle (Regex ile)
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
    
    exclude_cols = ['TARİH', 'SAAT', 'GRUP', 'MACSONUCU', 'TAKIM1', 'TAKIM2', '1', '0', '2']
    participants = [c for c in df.columns if c not in exclude_cols and not c.startswith('Unnamed')]

    if st.session_state.authenticated:
        for idx, row in df.iterrows():
            m_label = f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}"
            results[str(idx)] = st.sidebar.selectbox(
                m_label, 
                options=["Oynanmadı", "1", "0", "2"], 
                index=["Oynanmadı", "1", "0", "2"].index(results.get(str(idx), "Oynanmadı")),
                key=f"match_{idx}"
            )
        
        if st.sidebar.button("💾 Kaydet"):
            with open(RESULT_FILE, "w") as f:
                json.dump(results, f)
            st.rerun()

    scores = {p: 0.0 for p in participants}
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            idx = int(idx_str)
            row = df.iloc[idx]
            try:
                odd = float(row[res])
                for p in participants:
                    if str(row[p]) == res:
                        scores[p] += odd
            except: 
                continue

    lb = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    st.dataframe(lb.sort_values('Toplam Puan', ascending=False).reset_index(drop=True), use_container_width=True)

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
