import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")
st.title("🏆 HKED Tahmin Turnuvası Canlı Puan Durumu")

@st.cache_data
def load_data():
    df = pd.read_excel("HKED.xlsx")
    return df

try:
    df = load_data()
    
    # Maç Sonuçlarını Girme Alanı (Admin Paneli)
    st.sidebar.header("⚙️ Maç Sonuçlarını Girin")
    st.sidebar.write("Maçlar sonuçlandıkça buradan güncelleyin:")

    results = {}
    participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT ', 'CENK']
    scores = {p.strip(): 0.0 for p in participants}

    # İlk 2 maç oynandığı için varsayılan olarak seçili getirelim
    default_results = {0: "1", 1: "1"} 

    for index, row in df.iterrows():
        try:
            tarih_str = pd.to_datetime(row['TARİH']).strftime('%d.%m.%Y')
        except:
            tarih_str = str(row['TARİH'])
            
        match_label = f"{row['TAKIM - 1']} - {row['TAKIM - 2']} ({tarih_str})"
        default_val = default_results.get(index, "Oynanmadı")
        
        res = st.sidebar.selectbox(
            f"{match_label}", 
            options=["Oynanmadı", "1", "0", "2"], 
            index=["Oynanmadı", "1", "0", "2"].index(default_val),
            key=f"match_{index}"
        )
        if res != "Oynanmadı":
            results[index] = int(res)

    # Puan Hesaplama Motoru
    for idx, res in results.items():
        row = df.iloc[idx]
        odd = float(row[res]) 
        
        for p in participants:
            p_clean = p.strip()
            if int(row[p]) == res:
                scores[p_clean] += odd

    # Puan Durumu Tablosunu Oluşturma
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    # Ekrana Yazdırma
    st.subheader("📊 Güncel Sıralama")
    st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)

    st.subheader("📅 Tüm Fikstür ve Tahminler")
    st.dataframe(df)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
