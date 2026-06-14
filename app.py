import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# --- KALICI KAYIT VE YÜKLEME ---
RESULT_FILE = "sonuclar.json"

def load_results():
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_results(results):
    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

@st.cache_data
def load_data():
    df = pd.read_excel("HKED.xlsx")
    # Sütun isimlerindeki tüm boşlukları kaldırır, böylece "YİĞİT " ile "YİĞİT" aynı olur
    df.columns = df.columns.str.strip()
    return df

# --- OTURUM YÖNETİMİ ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

st.title("🏆 HKED Tahmin Turnuvası Canlı Puan Durumu")

# --- YETKİLENDİRME (ŞİFRE) ---
with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if not st.session_state.authenticated:
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if password == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Hatalı Şifre!")
    else:
        st.success("Admin girişi başarılı.")
        if st.button("Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()

# --- ANA MANTIK ---
try:
    df = load_data()
    results = load_results()
  # Listeyi boşluksuz tanımlayın
participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

# Puan hesaplarken de strip() kullanarak garantiye alın
for p in participants:
    # row[p] kısmında hata alıyorsanız, p'nin Excel'deki başlıkla aynı olduğundan emin olun
    if int(row[p.strip()]) == int(res): 
        scores[p.strip()] += odd

    # Admin ise sonuçları güncelle
    if st.session_state.authenticated:
        st.sidebar.write("Maç sonuçlarını güncelleyin:")
        for index, row in df.iterrows():
            match_label = f"{row['TAKIM - 1']} - {row['TAKIM - 2']}"
            current_val = results.get(str(index), "Oynanmadı")
            
            res = st.sidebar.selectbox(
                match_label, 
                options=["Oynanmadı", "1", "0", "2"], 
                index=["Oynanmadı", "1", "0", "2"].index(current_val),
                key=f"match_{index}"
            )
            results[str(index)] = res
        
        if st.sidebar.button("💾 Değişiklikleri Kaydet"):
            save_results(results)
            st.sidebar.success("Kayıt tamamlandı!")
            st.rerun()

    # Puan Hesaplama
    for idx_str, res in results.items():
        if res != "Oynanmadı":
            idx = int(idx_str)
            row = df.iloc[idx]
            odd = float(row[int(res)])
            for p in participants:
                if int(row[p.strip()]) == int(res):
                    scores[p.strip()] += odd

    # Tablolar
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    st.subheader("📊 Güncel Sıralama")
    st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)
    
    with st.expander("📅 Fikstürü Görüntüle"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
