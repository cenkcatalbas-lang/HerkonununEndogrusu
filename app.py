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

st.set_page_config(page_title="HKED Turnuva", layout="wide", page_icon="🏆")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');
html, body, [class*="css"] { background-color: #0f0c29 !important; color: white !important; }
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
.big-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.5rem;
    text-align: center;
    background: linear-gradient(90deg, #FFD700, #FF6B35, #FF0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
}
.sub { text-align:center; color:#aaa; letter-spacing:2px; margin-bottom:1.5rem; }
.card {
    border-radius: 14px;
    padding: 16px 22px;
    margin: 8px 0;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.c1 { background: linear-gradient(135deg,#FFD700,#FF8C00); color:#000; font-size:1.3rem; }
.c2 { background: linear-gradient(135deg,#3a3a3a,#555); color:#ddd; }
.c3 { background: linear-gradient(135deg,#2a1a0a,#5c3d1a); color:#cd7f32; }
.cx { background: rgba(255,255,255,0.04); color:#888; border:1px solid #333; }
.roast {
    font-style: italic; font-size: 0.88rem;
    padding: 10px 16px; border-radius: 8px; margin-bottom: 6px;
    border-left: 3px solid;
}
.r1 { background:rgba(255,215,0,0.07); border-color:#FFD700; color:#FFD700; }
.rx { background:rgba(255,50,50,0.07); border-color:#ff3333; color:#ff6666; }
.prob-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 6px; height: 12px; margin-top: 6px;
}
.stButton>button {
    background: linear-gradient(90deg,#FFD700,#FF6B35);
    color: #000; font-weight: 700; border: none; border-radius: 8px;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px; padding: 10px;
    border: 1px solid rgba(255,255,255,0.1);
}
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
            with open(RESULT_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

ROASTS = {
    1: ["TANRI MISALI HÜKÜM SÜRÜYOR 👑 Diğerleri senin gölgeni bile göremez.",
        "Rakipler bu ismi duymaktan titremeye başladı. Haklılar.",
        "Tahmin makinesi. Diğerleri ne yapıyor ki zaten?"],
    2: ["İkinci olmak; birinci OLAMAMAKtır. Ama ne yaparsın, bu senin tavanın.",
        "Zirveden bir adım uzakta... ya da onu hiç göremeyecek kadar mı?",
        "Gümüş madalya: altın olmak için YETERSİZ olduğunun kanıtı."],
    3: ["Üçüncü olmak yarı-başarısız olmaktır. Tebrikler sanırım? 🥉",
        "Podiyuma zar zor tutunuyor. Aşağı bakma, görünce üzülürsün.",
        "Bronz. Gurur duymak için sebebin yok, ama alışmışsındır zaten."],
    4: ["4. sıra. Resmen orta halli başarısızlık. Ne ön ne son, sadece VAR.",
        "Veriye bakılırsa maçları tahmin etmek yerine uyumuş.",
        "Kim olduğunu hatırlatmaya gerek yok, çünkü kimse hatırlamıyor zaten."],
    5: ["SONUNCU. 💀 Bu sonucu kelimelerle anlatmak acı verici.",
        "Turnuvada varlığından kimse haberdar değildi, skor da bunu kanıtlıyor.",
        "Tebrikler! En değersiz tahminler ödülünü kazandın. Kupa yok tabii. 🗑️"]
}

def get_roast(rank, total):
    key = rank if rank <= 3 else (5 if rank == total else 4)
    return random.choice(ROASTS[key])

def win_probability(scores):
    """Puana oransal + küçük rastgele gürültü ile olasılık hesapla (hafif)."""
    total = sum(scores.values())
    if total == 0:
        n = len(scores)
        return {p: 1/n for p in scores}
    return {p: s/total for p, s in scores.items()}

def remaining_adjusted_prob(scores, df, results, participant_names):
    """
    Kalan maç sayısına göre mevcut skoru yumuşat:
    Az maç kaldıysa mevcut puan belirleyici,
    Çok maç kaldıysa herkesin şansı biraz eşitlenir.
    """
    total_matches = len(df)
    played = sum(1 for v in results.values() if v != "Oynanmadı")
    remaining = total_matches - played

    base_prob = win_probability(scores)

    # Kalan maç oranı: 0=bitti, 1=hiç oynanmadı
    ratio = remaining / total_matches if total_matches > 0 else 0

    # Uniform dağılım (herkes eşit)
    uniform = {p: 1/len(participant_names) for p in participant_names}

    # Karıştır: mevcut puana göre + kalan maçların belirsizliği
    alpha = 1 - ratio  # az kalan = mevcut puan daha belirleyici
    final = {p: alpha * base_prob[p] + (1 - alpha) * uniform[p] for p in participant_names}

    # Normalize
    s = sum(final.values())
    return {p: v/s for p, v in final.items()}, remaining

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Admin Paneli")
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Yanlış şifre!")
    else:
        if st.button("Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()

        st.write("---")
        df_temp = load_data()
        results_admin = load_results()

        for idx, row in df_temp.iterrows():
            m_label = f"{row.get('TAKIM1','T1')} - {row.get('TAKIM2','T2')}"
            results_admin[str(idx)] = st.selectbox(
                m_label, ["Oynanmadı","1","0","2"],
                index=["Oynanmadı","1","0","2"].index(results_admin.get(str(idx),"Oynanmadı")),
                key=f"match_{idx}"
            )

        if st.button("💾 Kaydet"):
            with open(RESULT_FILE, "w") as f:
                json.dump(results_admin, f)
            st.cache_data.clear()
            st.success("Kaydedildi!")
            st.rerun()

# --- ANA BÖLÜM ---
st.markdown('<div class="big-title">🏆 HKED TAHMİN TURNUVASI 🏆</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">KİM KAZANIR? KİM EZİLİR? HERKES YARGILANIR.</div>', unsafe_allow_html=True)

try:
    df = load_data()
    results = load_results()

    # Puan hesapla
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
                except:
                    continue

    played = sum(1 for v in results.values() if v != "Oynanmadı")
    remaining = len(df) - played

    # Metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("⚽ Toplam Maç", len(df))
    c2.metric("✅ Oynanan", played)
    c3.metric("⏳ Kalan", remaining)

    st.markdown("---")

    # Sıralama
    sorted_p = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_p = len(sorted_p)

    rank_icons = {1:"👑",2:"🥈",3:"🥉"}
    fire_icons = {1:"🔥🔥🔥",2:"🔥🔥",3:"🔥"}
    card_cls  = {1:"c1",2:"c2",3:"c3"}

    st.markdown("### 🔥 ATEŞ SIRALAMASI")

    for rank, (name, score) in enumerate(sorted_p, 1):
        icon = rank_icons.get(rank, "💩" if rank == total_p else "😐")
        fire = fire_icons.get(rank, "🧊" if rank == total_p else "💧")
        cls  = card_cls.get(rank, "cx")
        roast = get_roast(rank, total_p)
        rcls = "r1" if rank == 1 else "rx"

        st.markdown(f"""
        <div class="card {cls}">
            <span>{fire} #{rank} {icon} {name}</span>
            <span>{score:.2f} puan</span>
        </div>
        <div class="roast {rcls}">💬 {roast}</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Bar chart — st.bar_chart (hafif)
    st.markdown("### 📊 PUAN TABLOSU")
    chart_df = pd.DataFrame(
        {"Puan": [scores[p] for p in [x[0] for x in sorted_p]]},
        index=[x[0] for x in sorted_p]
    )
    st.bar_chart(chart_df, height=300)

    st.markdown("---")

    # Kazanma olasılığı
    st.markdown("### 🎯 TURNUVA SONU KAZANMA OLASILIKLARI")
    st.caption("Kalan maç sayısı hesaba katılarak ağırlıklı olasılık yöntemiyle hesaplanmıştır.")

    probs, n_rem = remaining_adjusted_prob(scores, df, results, PARTICIPANT_NAMES)
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    for rank, (name, prob) in enumerate(sorted_probs, 1):
        pct = prob * 100
        if pct > 50:   yorum = "ÖLÜMSÜZ 👑"
        elif pct > 30: yorum = "KUVVETLİ ADAY 🔥"
        elif pct > 15: yorum = "ŞANSI VAR 🍀"
        elif pct > 5:  yorum = "ZORLANACAK 😬"
        else:          yorum = "UMUT YOK 💀"

        color = "#FFD700" if rank==1 else ("#aaa" if rank==2 else ("#cd7f32" if rank==3 else "#555"))

        st.markdown(f"""
        <div style="padding:12px 16px; margin:6px 0; background:rgba(255,255,255,0.04);
                    border-radius:10px; border-left:4px solid {color};">
            <div style="display:flex; justify-content:space-between;">
                <span style="color:{color}; font-weight:700;">#{rank} {name}</span>
                <span style="color:white; font-weight:700;">{pct:.1f}% — {yorum}</span>
            </div>
            <div class="prob-bar-bg">
                <div style="background:{color}; width:{min(pct,100):.0f}%; height:12px; border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Maç sonuçları
    st.markdown("### ⚽ GİRİLEN MAÇ SONUÇLARI")
    match_list = []
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            row = df.iloc[int(idx_str)]
            match_list.append({
                "Maç": f"{row.get('TAKIM1','T1')} - {row.get('TAKIM2','T2')}",
                "Sonuç": res
            })
    if match_list:
        st.dataframe(pd.DataFrame(match_list), use_container_width=True)
    else:
        st.info("Henüz sonuç girilmemiş.")

    st.markdown("### 📅 TÜM FİKSTÜR")
    with st.expander("Fikstürü Görüntüle"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Hata: {e}")
    st.exception(e)
