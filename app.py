import streamlit as st
import pandas as pd
import json
import os
import re

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANT_NAMES = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# --- FONKSİYONLAR ---
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
        except:
            return {}
    return {}

# --- ARAYÜZ ---
st.title("🏆 HKED Tahmin Turnuvası")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Sidebar: Admin Paneli
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
            
        st.write("---")
        df_temp = load_data()
        results = load_results()
        
        for idx, row in df_temp.iterrows():
            m_label = f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}"
            results[str(idx)] = st.selectbox(
                m_label, ["Oynanmadı", "1", "0", "2"], 
                index=["Oynanmadı", "1", "0", "2"].index(results.get(str(idx), "Oynanmadı")),
                key=f"match_{idx}"
            )
        
        if st.button("💾 Değişiklikleri Kaydet"):
            with open(RESULT_FILE, "w") as f:
                json.dump(results, f)
            st.success("Kayıt başarılı!")
            st.rerun()

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

    # Puan Tablosu
    st.subheader("📊 Güncel Sıralama")
    lb = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    lb = lb.sort_values('Toplam Puan', ascending=False).reset_index(drop=True)
    lb.index = range(1, len(lb) + 1)
    st.dataframe(lb.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)

    # --- YENİ EKLENEN: MAÇ SONUÇLARI TABLOSU ---
    st.subheader("⚽ Girilen Maç Sonuçları")
    match_list = []
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            row = df.iloc[int(idx_str)]
            match_list.append({
                "Maç": f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}",
                "Sonuç": res
            })
    
    if match_list:
        st.table(pd.DataFrame(match_list))
    else:
        st.info("Henüz girilmiş bir sonuç bulunmuyor.")

    # Fikstür
    st.subheader("📅 Tüm Fikstür")
    with st.expander("Fikstürü Görüntüle"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
# Puan Tablosu ve Etiketleme
    lb = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    lb = lb.sort_values('Toplam Puan', ascending=False).reset_index(drop=True)
    
    # Etiketleri ekleyen fonksiyon
    def get_rank_label(rank):
        labels = {
            0: "Normal", 
            1: "Tecrübesiz", 
            2: "Aptal", 
            3: "Gerizekalı",
            4: "Beyinsiz"
        }
        return labels.get(rank, "---")

    lb['Durum'] = [get_rank_label(i) for i in range(len(lb))]
    lb.index = range(1, len(lb) + 1)
    
    # Tabloyu görselleştirme
    st.dataframe(lb.style.format({"Toplam Puan": "{:.2f}"}).background_gradient(cmap="Greens"), use_container_width=True)
