import streamlit as st
import pandas as pd
import json
import os
import re
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- AYARLAR ---
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANT_NAMES = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide", page_icon="🏆")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }

    .main-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 4rem;
        text-align: center;
        background: linear-gradient(90deg, #FFD700, #FF6B35, #FF0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        letter-spacing: 4px;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }

    .rank-card {
        border-radius: 16px;
        padding: 20px 24px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }

    .rank-1 {
        background: linear-gradient(135deg, #FFD700, #FF8C00);
        color: #000;
        font-size: 1.4rem;
        border: 2px solid #FFD700;
    }

    .rank-2 {
        background: linear-gradient(135deg, #2c2c2c, #444);
        color: #ccc;
        border: 1px solid #555;
    }

    .rank-3 {
        background: linear-gradient(135deg, #1a1a2e, #333);
        color: #aaa;
        border: 1px solid #444;
    }

    .rank-other {
        background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
        color: #666;
        border: 1px solid #222;
        opacity: 0.85;
    }

    .roast-box {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 8px 0;
        font-style: italic;
        font-size: 0.92rem;
        border-left: 4px solid;
    }

    .roast-1 { background: rgba(255,215,0,0.08); border-color: #FFD700; color: #FFD700; }
    .roast-other { background: rgba(255,50,50,0.08); border-color: #ff3333; color: #ff6666; }

    .prob-bar-container {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }

    .section-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 2rem;
        letter-spacing: 3px;
        color: #FFD700;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .confetti-text {
        text-align: center;
        font-size: 3rem;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1); }
    }

    .fire-rank {
        font-size: 1.5rem;
    }

    .stSelectbox label, .stTextInput label, .stButton button {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #FF6B35);
        color: black;
        font-weight: 700;
        border: none;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #FF6B35, #FFD700);
        color: black;
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

def get_rank_emoji(rank, total):
    if rank == 1: return "👑"
    if rank == 2: return "🥈"
    if rank == 3: return "🥉"
    if rank == total: return "💩"
    return "😐"

def get_fire_level(rank, total):
    if rank == 1: return "🔥🔥🔥"
    if rank == 2: return "🔥🔥"
    if rank == 3: return "🔥"
    if rank == total: return "🧊"
    return "💧"

ROASTS = {
    1: [
        "TANRI MISALI HÜKÜM SÜRÜYOR. Diğerleri senin gölgende ezilmeye devam edecek.",
        "Rakipler bu ismi duymaktan titremeye başladı bile.",
        "Tahmin makinesine dönmüş. Diğerleri ne yapıyor ki zaten?"
    ],
    2: [
        "İkinci olmak; birinci olmayan demektir. Ama ne yaparsın, bu da senin kaderin.",
        "Zirveden bir adım uzakta... ya da onu hiç göremeyecek kadar mı?",
        "Gümüş madalya, altın olmak için yeterli olmadığının hatırasıdır."
    ],
    3: [
        "Üçüncü olmak, yarı-başarısız olmaktır. Tebrikler sanırım?",
        "Podiyuma zar zor tutunuyor. Aşağı bak, köhnemiş rakiplerin orada.",
        "Bronz? Evet, bronz. Gurur duymak için yeterli bir sebebin yok."
    ],
    4: [
        "Bu sıralamayı görmek için kalp krizine hazırlan.",
        "Veriye bakılırsa maçları tahmin etmek yerine çay içip uyumuş.",
        "4. sıra. Resmen orta halli başarısızlık. Ne ön, ne son."
    ],
    5: [
        "SONUNCU. 💀 Bu sonucu kelimelerle anlatmak bile zor.",
        "Turnuvada varlığından kimse haberdar değil gibiydi, skor da bunu kanıtlıyor.",
        "Tebrikler! En değersiz tahminler ödülünü kazandın. Kupa yok tabii."
    ]
}

def get_roast(rank, total):
    import random
    if rank == 1:
        return random.choice(ROASTS[1])
    elif rank == 2:
        return random.choice(ROASTS[2])
    elif rank == 3:
        return random.choice(ROASTS[3])
    elif rank == total:
        return random.choice(ROASTS[5])
    else:
        return random.choice(ROASTS[4])

def calculate_win_probability(scores, df, results, participant_names):
    """
    Kalan maçları simüle ederek kazanma olasılığını hesaplar.
    Monte Carlo simülasyonu: her kalan maç için olası sonuçları (1,0,2) dene,
    her katılımcının tahminlerine göre puan ekle, bunu N kez tekrarla.
    """
    N_SIMULATIONS = 5000

    # Kalan maçları bul
    remaining = []
    for idx in range(len(df)):
        idx_str = str(idx)
        if results.get(idx_str, "Oynanmadı") == "Oynanmadı":
            remaining.append(idx)

    if not remaining:
        # Turnuva bitti, mevcut skora göre oransal hesapla
        total = sum(scores.values())
        if total == 0:
            prob = {p: 1/len(participant_names) for p in participant_names}
        else:
            prob = {p: scores[p]/total for p in participant_names}
        return prob, 0

    win_counts = {p: 0 for p in participant_names}

    for _ in range(N_SIMULATIONS):
        sim_scores = scores.copy()
        for idx in remaining:
            row = df.iloc[idx]
            # Rastgele bir sonuç seç
            sim_result = np.random.choice(["1", "0", "2"])
            try:
                odd = float(row[sim_result])
                for p in participant_names:
                    if str(row[p]) == sim_result:
                        sim_scores[p] += odd
            except:
                pass
        # Bu simülasyonda kazananı bul
        winner = max(sim_scores, key=sim_scores.get)
        win_counts[winner] += 1

    prob = {p: win_counts[p] / N_SIMULATIONS for p in participant_names}
    return prob, len(remaining)

# --- BAŞLIK ---
st.markdown('<div class="main-title">🏆 HKED TAHMİN TURNUVASI 🏆</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">KİM KAZANIR? KİM EZİLİR? HERKESE AÇIK YARGILAMA.</div>', unsafe_allow_html=True)

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
            st.cache_data.clear()
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
                except:
                    continue

    # Sıralama
    sorted_participants = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_p = len(sorted_participants)

    # --- ÖZET METRİKLER ---
    played = sum(1 for v in results.values() if v != "Oynanmadı")
    total_matches = len(df)
    remaining_matches = total_matches - played

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚽ Toplam Maç", total_matches)
    with col2:
        st.metric("✅ Oynanan Maç", played)
    with col3:
        st.metric("⏳ Kalan Maç", remaining_matches)

    st.markdown("---")

    # --- SIRALAMAYI GÖSTER ---
    st.markdown('<div class="section-title">🔥 ATEŞ SIRALAMASI</div>', unsafe_allow_html=True)

    leader_name = sorted_participants[0][0]

    # Konfeti efekti için
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.3 },
        colors: ['#FFD700', '#FF6B35', '#FF0080', '#00FFFF']
    });
    </script>
    """
    st.components.v1.html(confetti_js, height=0)

    for rank, (name, score) in enumerate(sorted_participants, 1):
        rank_class = "rank-1" if rank == 1 else ("rank-2" if rank == 2 else ("rank-3" if rank == 3 else "rank-other"))
        emoji = get_rank_emoji(rank, total_p)
        fire = get_fire_level(rank, total_p)
        roast = get_roast(rank, total_p)
        roast_class = "roast-1" if rank == 1 else "roast-other"

        st.markdown(f"""
        <div class="rank-card {rank_class}">
            <span class="fire-rank">{fire} #{rank} {emoji} {name}</span>
            <span>{score:.2f} puan</span>
        </div>
        <div class="roast-box {roast_class}">
            💬 {roast}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- BAR CHART ---
    st.markdown('<div class="section-title">📊 PUAN TABLOSU</div>', unsafe_allow_html=True)

    names_sorted = [x[0] for x in sorted_participants]
    scores_sorted = [x[1] for x in sorted_participants]
    colors = ['#FFD700' if i == 0 else '#FF6B35' if i == 1 else '#FF0080' if i == 2 else '#444' for i in range(len(names_sorted))]

    fig_bar = go.Figure(go.Bar(
        x=names_sorted,
        y=scores_sorted,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{s:.2f}" for s in scores_sorted],
        textposition='outside',
        textfont=dict(color='white', size=14, family='Inter')
    ))

    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color='white', family='Inter'),
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color='white')),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#aaa')),
        margin=dict(t=40, b=20, l=20, r=20),
        height=380,
        showlegend=False,
        bargap=0.35
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # --- KAZANMA OLASILIĞI ---
    st.markdown('<div class="section-title">🎯 TURNUVA SONU KAZANMA OLASILIKLARI</div>', unsafe_allow_html=True)
    st.caption("Monte Carlo simülasyonu ile kalan maçlar hesaba katılarak hesaplanmıştır.")

    with st.spinner("Simülasyon hesaplanıyor..."):
        win_probs, n_remaining = calculate_win_probability(scores, df, results, PARTICIPANT_NAMES)

    # Olasılıkları sırala
    sorted_probs = sorted(win_probs.items(), key=lambda x: x[1], reverse=True)

    # Pasta grafiği
    prob_names = [x[0] for x in sorted_probs]
    prob_vals = [x[1] * 100 for x in sorted_probs]
    pie_colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#444444', '#222222']

    fig_pie = go.Figure(go.Pie(
        labels=prob_names,
        values=prob_vals,
        hole=0.45,
        marker=dict(colors=pie_colors[:len(prob_names)], line=dict(color='#000', width=2)),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='%{label}: %{value:.1f}%<extra></extra>'
    ))

    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        annotations=[dict(
            text=f'<b>{n_remaining}</b><br>kalan maç',
            x=0.5, y=0.5,
            font=dict(size=16, color='white'),
            showarrow=False
        )]
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # Olasılık listesi
    for rank, (name, prob) in enumerate(sorted_probs, 1):
        bar_fill = int(prob * 100)
        color = "#FFD700" if rank == 1 else ("#aaa" if rank == 2 else ("#cd7f32" if rank == 3 else "#444"))
        yorum = "ÖLÜMSÜZ 👑" if prob > 0.5 else ("ŞANSLI 🍀" if prob > 0.25 else ("ZORLANACAK 😬" if prob > 0.1 else "UMUTLAR YOK 💀"))
        st.markdown(f"""
        <div style="margin: 8px 0; padding: 12px 18px; background: rgba(255,255,255,0.04);
                    border-radius: 10px; border-left: 4px solid {color};">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="font-weight:700; color:{color}; font-size:1rem;">#{rank} {name}</span>
                <span style="color:white; font-weight:700; font-size:1.1rem;">{prob*100:.1f}% — {yorum}</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius:6px; height:10px;">
                <div style="background:{color}; width:{bar_fill}%; height:10px; border-radius:6px;
                            transition: width 1s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- MAÇ SONUÇLARI ---
    st.markdown('<div class="section-title">⚽ GİRİLEN MAÇ SONUÇLARI</div>', unsafe_allow_html=True)
    match_list = []
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            row = df.iloc[int(idx_str)]
            match_list.append({
                "Maç": f"{row.get('TAKIM1', 'T1')} - {row.get('TAKIM2', 'T2')}",
                "Sonuç": res
            })

    if match_list:
        st.dataframe(pd.DataFrame(match_list), use_container_width=True)
    else:
        st.info("Henüz girilmiş bir sonuç bulunmuyor.")

    # --- FİKSTÜR ---
    st.markdown('<div class="section-title">📅 TÜM FİKSTÜR</div>', unsafe_allow_html=True)
    with st.expander("Fikstürü Görüntüle"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
    st.exception(e)
