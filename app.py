import streamlit as st
import pandas as pd
import json
import os
import re

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANT_NAMES = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva Takip", page_icon="🏆", layout="wide")

# --- FONKSİYONLAR (Aynı) ---
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    df.columns = [re.sub(r'[^a-zA-ZçÇğĞıİöÖşŞüÜ0-9]', '', str(c)).upper() for c in df.columns]
    return df

def load_results():
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

# --- ARAYÜZ VE GÖRSELLİK ---
st.title("🏆 HKED Tahmin Turnuvası")
st.markdown("---")

# --- ANA MANTIK ---
try:
    df = load_data()
    results = load_results()

    # Puan Hesaplama
    scores = {p: 0.0 for p in PARTICIPANT_NAMES}
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            idx = int(idx_str)
            if idx < len(df):
                row = df.iloc[idx]
                try:
                    odd = float(row[res])
                    for p in PARTICIPANT_NAMES:
                        if str(row[p]) == res:
                            scores[p] += odd
                except: continue

    # GÖRSEL: Puan Durumu Kartları (En yüksek puanlıları öne çıkar)
    st.subheader("📊 Canlı Skor Tablosu")
    cols = st.columns(len(PARTICIPANT_NAMES))
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, score) in enumerate(sorted_scores):
        cols[i].metric(label=name, value=f"{score:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detaylı Tablo
    lb = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    lb = lb.sort_values('Toplam Puan', ascending=False).reset_index(drop=True)
    lb.index = range(1, len(lb) + 1)
    st.dataframe(lb.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)

    # MAÇ SONUÇLARI (Görsel Liste)
    st.subheader("⚽ Girilen Maç Sonuçları")
    match_data = []
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            row = df.iloc[int(idx_str)]
            match_data.append({"Maç": f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}", "Sonuç": res})
    
    if match_data:
        st.table(pd.DataFrame(match_data))
    else:
        st.info("Henüz sonuç girilmedi.")

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
