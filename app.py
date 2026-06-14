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

.stApp {
    background: #f0f2f6;
}

/* Tüm yazılar koyu */
body, p, span, div, label, .stMarkdown, .stText {
    color: #1a1a2e !important;
}

.big-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.2rem;
    text-align: center;
    color: #1a1a2e;
    letter-spacing: 4px;
    text-shadow: none;
    margin-bottom: 0.1rem;
}

.sub {
    text-align: center;
    color: #666688;
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}

.card {
    border-radius: 12px;
    padding: 14px 20px;
    margin: 6px 0 2px 0;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 1. — altın arka plan, KESİNLİKLE siyah yazı */
.c1 {
    background: #FFD700;
    color: #000000 !important;
    font-size: 1.2rem;
    border: none;
    box-shadow: 0 2px 8px rgba(255,215,0,0.3);
}
.c1 * { color: #000000 !important; }

/* 2. — beyaz arka plan, koyu yazı, gümüş border */
.c2 {
    background: #ffffff;
    color: #222222 !important;
    border: 2px solid #aaaaaa;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.c2 * { color: #222222 !important; }

/* 3. — açık turuncu arka plan, koyu yazı */
.c3 {
    background: #fff3e0;
    color: #5c3200 !important;
    border: 2px solid #b87333;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.c3 * { color: #5c3200 !important; }

/* 4-5 — açık gri arka plan, orta koyu yazı */
.cx {
    background: #e8eaf0;
    color: #555577 !important;
    border: 1px solid #ccccdd;
}
.cx * { color: #555577 !important; }

.roast {
    font-style: italic;
    font-size: 0.88rem;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    border-left: 3px solid;
    font-weight: 500;
}

/* 1. roast — sarı arka plan, koyu yazı */
.r1 {
    background: #fffbe6;
    border-color: #e6b800;
    color: #7a5c00 !important;
}
.r1 * { color: #7a5c00 !important; }

/* Diğer roastlar — açık kırmızı arka plan, koyu yazı */
.rx {
    background: #fff0f0;
    border-color: #cc2222;
    color: #aa1111 !important;
}
.rx * { color: #aa1111 !important; }

.prob-row {
    padding: 12px 16px;
    margin: 6px 0;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.prob-name {
    font-weight: 700;
    font-size: 1rem;
}

.prob-yorum {
    font-weight: 700;
    font-size: 0.95rem;
    color: #1a1a2e !important;
}

.prob-bar-bg {
    background: #dde0ea;
    border-radius: 6px;
    height: 12px;
    margin-top: 7px;
}

.section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.6rem;
    color: #1a1a2e;
    letter-spacing: 2px;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
}

/* Metrik kutuları */
div[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #dde0ea;
    padding: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
div[data-testid="metric-container"] label {
    color: #666688 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #1a1a2e !important;
    font-size: 1.8rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #e4e7f0;
    border-right: 1px solid #ccccdd;
}
section[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}

/* Buton */
.stButton > button {
    background: #1a1a2e;
    color: #ffffff;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
}
.stButton > button:hover {
    background: #2e2e4e;
    color: #ffffff;
}

/* Tablo */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* Input alanları */
.stTextInput input {
    background: #1a1a2e !important;
    color: #ffffff !important;
    border: 1px solid #444466 !important;
}

/* Selectbox — seçili değer ve dropdown yazısı siyah */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] span {
    color: #000000 !important;
}
div[data-baseweb="select"] > div {
    background: #ffffff !important;
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
    1: [
        "TANRI MISALI HÜKÜM SÜRÜYOR 👑 Diğerleri senin gölgeni bile göremez.",
        "Rakipler bu ismi duymaktan titremeye başladı. Haklılar.",
        "Tahmin makinesi. Diğerleri ne yapıyor ki zaten?"
    ],
    2: [
        "İkinci olmak; birinci OLAMAMAKtır. Ama ne yaparsın, bu senin tavanın.",
        "Zirveden bir adım uzakta... ya da onu hiç göremeyecek kadar mı?",
        "Gümüş madalya: altın olmak için YETERSİZ olduğunun kanıtı."
    ],
    3: [
        "Üçüncü olmak yarı-başarısız olmaktır. Tebrikler sanırım? 🥉",
        "Podiyuma zar zor tutunuyor. Aşağı bakma, görünce üzülürsün.",
        "Bronz. Gurur duymak için sebebin yok, ama alışmışsındır zaten."
    ],
    4: [
        "4. sıra. Resmen orta halli başarısızlık. Ne ön ne son, sadece VAR.",
        "Veriye bakılırsa maçları tahmin etmek yerine uyumuş.",
        "Kim olduğunu hatırlatmaya gerek yok, çünkü kimse hatırlamıyor zaten."
    ],
    5: [
        "SONUNCU. 💀 Bu sonucu kelimelerle anlatmak bile acı verici.",
        "Turnuvada varlığından kimse haberdar değildi, skor da bunu kanıtlıyor.",
        "Tebrikler! En değersiz tahminler ödülünü kazandın. Kupa yok tabii. 🗑️"
    ]
}

def get_roast(rank, total):
    key = rank if rank <= 3 else (5 if rank == total else 4)
    return random.choice(ROASTS[key])

def win_probability(scores, df, results, participant_names):
    total_matches = len(df)
    played = sum(1 for v in results.values() if v != "Oynanmadı")
    remaining = total_matches - played
    ratio = remaining / total_matches if total_matches > 0 else 0

    total_score = sum(scores.values())
    if total_score == 0:
        base = {p: 1/len(participant_names) for p in participant_names}
    else:
        base = {p: scores[p]/total_score for p in participant_names}

    uniform = {p: 1/len(participant_names) for p in participant_names}
    alpha = 1 - ratio
    final = {p: alpha * base[p] + (1 - alpha) * uniform[p] for p in participant_names}
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
    m1, m2, m3 = st.columns(3)
    m1.metric("⚽ Toplam Maç", len(df))
    m2.metric("✅ Oynanan", played)
    m3.metric("⏳ Kalan", remaining)

    st.markdown("---")

    sorted_p = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_p = len(sorted_p)

    rank_icons = {1:"👑", 2:"🥈", 3:"🥉"}
    fire_icons = {1:"🔥🔥🔥", 2:"🔥🔥", 3:"🔥"}
    card_cls   = {1:"c1", 2:"c2", 3:"c3"}

    st.markdown('<div class="section-title">🔥 ATEŞ SIRALAMASI</div>', unsafe_allow_html=True)

    for rank, (name, score) in enumerate(sorted_p, 1):
        icon = rank_icons.get(rank, "💩" if rank == total_p else "😐")
        fire = fire_icons.get(rank, "🧊" if rank == total_p else "💧")
        cls  = card_cls.get(rank, "cx")
        roast = get_roast(rank, total_p)
        if name == "YİĞİT":
            roast = "Buralar sana fazla aslanım, yallah 9gag'e 😂"
        rcls = "r1" if rank == 1 else "rx"

        st.markdown(f"""
        <div class="card {cls}">
            <span>{fire} #{rank} {icon} {name}</span>
            <span>{score:.2f} puan</span>
        </div>
        <div class="roast {rcls}">💬 {roast}</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">📊 PUAN TABLOSU</div>', unsafe_allow_html=True)
    chart_df = pd.DataFrame(
        {"Puan": [scores[x[0]] for x in sorted_p]},
        index=[x[0] for x in sorted_p]
    )
    st.bar_chart(chart_df, height=280)

    st.markdown("---")

    st.markdown('<div class="section-title">🎯 TURNUVA SONU KAZANMA OLASILIKLARI</div>', unsafe_allow_html=True)
    st.caption("Kalan maç belirsizliği hesaba katılarak ağırlıklı olasılık yöntemiyle hesaplanmıştır.")

    probs, n_rem = win_probability(scores, df, results, PARTICIPANT_NAMES)
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    prob_colors = {1:"#e6b800", 2:"#888888", 3:"#b87333"}

    for rank, (name, prob) in enumerate(sorted_probs, 1):
        pct = prob * 100
        if pct > 50:   yorum = "ÖLÜMSÜZ 👑"
        elif pct > 30: yorum = "KUVVETLİ ADAY 🔥"
        elif pct > 15: yorum = "ŞANSI VAR 🍀"
        elif pct > 5:  yorum = "ZORLANACAK 😬"
        else:          yorum = "UMUT YOK 💀"

        color = prob_colors.get(rank, "#555577")
        text_color = "#000000" if rank == 1 else "#ffffff"

        st.markdown(f"""
        <div class="prob-row" style="border-left: 4px solid {color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="prob-name" style="color:{color};">#{rank} {name}</span>
                <span class="prob-yorum">{pct:.1f}% — {yorum}</span>
            </div>
            <div class="prob-bar-bg">
                <div style="background:{color}; width:{min(pct,100):.0f}%; height:12px; border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">⚽ GİRİLEN MAÇ SONUÇLARI</div>', unsafe_allow_html=True)
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

    st.markdown('<div class="section-title">📅 TÜM FİKSTÜR</div>', unsafe_allow_html=True)
    with st.expander("Fikstürü Görüntüle"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Hata: {e}")
    st.exception(e)
