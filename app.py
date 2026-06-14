import streamlit as st
import pandas as pd
import json
import os
import re
import random

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANT_NAMES = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

# Sayfa ayarları en başta yapılmalı
st.set_page_config(page_title="HKED Turnuva", layout="wide", page_icon="🏆")

# CSS AYARLARI (Aydınlık ve ferah tema)
st.markdown("""
<style>
.stApp { background: #f4f4f9; }
body, p, span, div, label, .stMarkdown, .stText { color: #2e2e2e !important; }

.big-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.2rem;
    text-align: center;
    color: #1a1a1a;
    letter-spacing: 4px;
    margin-bottom: 0.1rem;
}
.sub { text-align: center; color: #555555; letter-spacing: 2px; margin-bottom: 1.5rem; font-size: 0.9rem; }

.card {
    border-radius: 12px; padding: 14px 20px; margin: 6px 0 2px 0;
    font-weight: 700; display: flex; justify-content: space-between;
    background: #ffffff; border: 1px solid #dcdcdc;
}
.roast {
    font-style: italic; padding: 10px 16px; border-radius: 8px;
    border-left: 3px solid #ffcc00; background: #fffdf0; color: #333 !important;
}
.section-title { font-size: 1.6rem; color: #1a1a1a; margin-top: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    df.columns = [re.sub(r'[^a-zA-ZçÇğĞıİöÖşŞüÜ0-9]', '', str(c)).upper() for c in df.columns]
    return df

def load_results():
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def get_roast(rank, total):
    roasts = {
        1: ["TANRI MISALI HÜKÜM SÜRÜYOR 👑", "Rakipler bu ismi duymaktan titriyor."],
        2: ["İkinci olmak; birinci OLAMAMAKtır.", "Zirveden bir adım uzakta."],
        3: ["Üçüncü olmak yarı-başarısız olmaktır.", "Bronzla yetiniyor."],
        4: ["4. sıra. Orta halli başarısızlık.", "Sadece var, o kadar."],
        5: ["SONUNCU. 💀 Acı verici.", "Bu tahminler biraz... beyinsizce."]
    }
    key = rank if rank <= 3 else (5 if rank == total else 4)
    return random.choice(roasts.get(key, ["İdare eder..."]))

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        if st.text_input("Şifre", type="password") == "1234":
            if st.button("Giriş Yap"): st.session_state.authenticated = True; st.rerun()
    else:
        if st.button("Çıkış Yap"): st.session_state.authenticated = False; st.rerun()
        df_temp = load_data()
        res_admin = load_results()
        for idx, row in df_temp.iterrows():
            res_admin[str(idx)] = st.selectbox(f"{row.get('TAKIM1','T1')} - {row.get('TAKIM2','T2')}", 
                                             ["Oynanmadı","1","0","2"], index=["Oynanmadı","1","0","2"].index(res_admin.get(str(idx),"Oynanmadı")))
        if st.button("💾 Kaydet"):
            with open(RESULT_FILE, "w") as f: json.dump(res_admin, f)
            st.success("Kaydedildi!"); st.rerun()

# --- ANA GÖVDE ---
st.markdown('<div class="big-title">🏆 HKED TAHMİN TURNUVASI</div>', unsafe_allow_html=True)
try:
    df = load_data()
    results = load_results()
    scores = {p: 0.0 for p in PARTICIPANT_NAMES}
    
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit() and int(idx_str) < len(df):
            row = df.iloc[int(idx_str)]
            if str(row.
