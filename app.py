import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"

st.set_page_config(page_title="HKED Turnuva", layout="wide")
st.title("🏆 HKED Tahmin Turnuvası")

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    df.columns = df.columns.str.strip()
    return df

# Veri yükleme
df = load_data()

# Katılımcıları belirle (Fikstür sütunlarını dışarıda bırak)
exclude_cols = ['TARİH', 'TAKIM - 1', 'TAKIM - 2', '1', '0', '2']
participants = [col for col in df.columns if col not in exclude_cols]

# 1. Mevcut sonuçları yükle (dosya yoksa boş sözlük)
if os.path.exists(RESULT_FILE):
    with open(RESULT_FILE, "r") as f:
        results = json.load(f)
else:
    results = {}

# 2. Sidebar: Maç sonuç girişi
st.sidebar.header("⚙️ Maç Sonuçları")
new_results = {}

for index, row in df.iterrows():
    match_label = f"{row['TAKIM - 1']} - {row['TAKIM - 2']}"
    current_res = results.get(str(index), "Oynanmadı")
    
    res = st.sidebar.selectbox(
        match_label,
        options=["Oynanmadı", "1", "0", "2"],
        index=["Oynanmadı", "1", "0", "2"].index(current_res),
        key=f"match_{index}"
    )
    new_results[str(index)] = res

# Kayıt Butonu
if st.sidebar.button("💾 Sonuçları Kaydet"):
    with open(RESULT_FILE, "w") as f:
        json.dump(new_results, f)
    st.sidebar.success("Kayıt başarılı!")
    st.rerun()

# 3. Puan Hesaplama
scores = {p: 0.0 for p in participants}
for idx_str, res in new_results.items():
    if res != "Oynanmadı":
        row = df.iloc[int(idx_str)]
        res_int = int(res)
        odd = float(row[res_int])
        for p in participants:
            if str(row[p]) == res:
                scores[p] += odd

# Puan tablosu
leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
leaderboard.index += 1

st.subheader("📊 Güncel Puan Durumu")
st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)
