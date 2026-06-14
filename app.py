import streamlit as st
import pandas as pd
import json
import os

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# --- FONKSİYONLAR ---
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    
    # 1. Tekrarlayan sütun isimlerini benzersiz yap
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '.' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols
    
    # 2. Sütun isimlerini temizle (Boşlukları al)
    df.columns = df.columns.str.strip()
    
    # 3. İsimsiz sütunları kaldır
    df = df.loc[:, df.columns.notna()]
    return df

def load_results():
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}

def save_results(results):
    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

# --- OTURUM VE GİRİŞ ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

st.title("🏆 HKED Tahmin Turnuvası Canlı Puan Durumu")

with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if not st.session_state.authenticated:
        password = st.text_input("Admin Şifresi", type="password")
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

# --- ANA PROGRAM ---
try:
    df = load_data()
    results = load_results()
    
    # Katılımcıları dinamik belirle (Sabit sütunlar dışındakileri al)
    fixed_cols = ['TARİH', 'SAAT', 'GRUP', 'MAÇ SONUCU', 'TAKIM - 1', 'TAKIM - 2', '1', '0', '2', 'nan']
    participants = [col for col in df.columns if col not in fixed_cols and not str(col).startswith('Unnamed')]

    # Admin ise sonuçları güncelleme alanı
    if st.session_state.authenticated:
        st.sidebar.write("---")
        st.sidebar.write("Maç sonuçlarını güncelleyin:")
        for index, row in df.iterrows():
            match_label = f"{row.get('TAKIM - 1', 'T1')} - {row.get('TAKIM - 2', 'T2')}"
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

    # Puan Hesaplama Motoru
    scores = {p: 0.0 for p in participants}
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            idx = int(idx_str)
            row = df.iloc[idx]
            odd = float(row[int(res)])
            
            for p in participants:
                # Sütun başlığı ile tahmin eşleşmesi
                if str(row[p]) == res:
                    scores[p] += odd

    # Puan tablosunu oluştur
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    st.subheader("📊 Güncel Sıralama")
    st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)
    
    with st.expander("📅 Fikstürü Görüntüle"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
