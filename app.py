import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="Bojxona Yig'imlari Kalkulyatori",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main { background-color: #f5f7fa; }
h1 {
    text-align: center; padding: 20px;
    background: linear-gradient(135deg, #1a3a6b 0%, #2563eb 100%);
    color: white; border-radius: 12px; margin-bottom: 25px;
}
h2 { color: #1a3a6b; border-bottom: 3px solid #2563eb; padding-bottom: 8px; }
.metric-card {
    background: white; padding: 18px; border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin: 8px 0;
    border-left: 4px solid #2563eb;
}
.info-box {
    background: #eff6ff; padding: 14px;
    border-left: 4px solid #2563eb; border-radius: 6px; margin: 10px 0;
}
.result-box {
    background: linear-gradient(135deg, #1a3a6b, #2563eb);
    color: white; padding: 20px; border-radius: 12px;
    text-align: center; margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Dollar kursini CBU dan olish ───
@st.cache_data(ttl=3600)
def get_usd_rate():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/{today}/"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data:
            return float(data[0]["Rate"]), data[0]["Date"], True
    except Exception:
        pass
    return 12900.0, "Avtomatik olinmadi", False

# ─── SIDEBAR ───
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Uzbekistan.svg", width=240)
    st.markdown("### 🏛️ O'zbekiston Respublikasi")
    st.markdown("**Vazirlar Mahkamasi qarori**")
    st.markdown("**№ 55, 31.01.2025**")
    st.divider()

    st.markdown("### 💰 BHM Sozlamalari")
    bhm = st.number_input(
        "BHM miqdori (so'm):",
        min_value=100000, max_value=2000000,
        value=340000, step=5000,
        help="Joriy yilga belgilangan rasmiy BHM miqdorini kiriting"
    )
    st.caption(f"Joriy BHM: **{bhm:,} so'm**")
    st.divider()

    st.markdown("### 💵 Dollar Kursi")
    usd_auto, usd_date, usd_ok = get_usd_rate()

    if usd_ok:
        st.success(f"✅ CBU kursi ({usd_date})")
        st.metric("1 USD", f"{usd_auto:,.0f} so'm")
        use_auto = st.checkbox("Avtomatik kursni ishlatish", value=True)
    else:
        st.warning("⚠️ CBU ma'lumotlari olinmadi")
        use_auto = False

    if use_auto and usd_ok:
        USD_RATE = usd_auto
    else:
        USD_RATE = float(st.number_input(
            "Kursni qo'lda kiriting (so'm):",
            min_value=5000, max_value=50000,
            value=int(usd_auto), step=50
        ))

    st.divider()
    st.markdown("### 📋 Bo'limlar")
    menu = st.radio("", [
        "🏠 Asosiy ma'lumot",
        "📋 Rasmiylashtiruv yig'imi",
        "🔄 Tranzit va maxsus rejimlar",
        "🏪 Ombor saqlash",
        "🚗 Avtomobil hamrohligi",
        "👤 Jismoniy shaxslar",
        "📜 Boshqa xizmatlar",
        "📊 Barcha stavkalar jadvali",
        "📈 Grafik tahlil",
    ], label_visibility="collapsed")

# ─── SARLAVHA ───
st.markdown("<h1>📦 Bojxona Yig'imlari Kalkulyatori </h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("💵 1 USD (CBU)", f"{USD_RATE:,.0f} so'm")
c2.metric("💰 BHM", f"{bhm:,} so'm")
c3.metric("📅 Kurs sanasi", usd_date if usd_ok else "Qo'lda")
c4.metric("📋 Qaror", "VM № 55 · 31.01.2025")
st.divider()

# ─── YORDAMCHI FUNKSIYALAR ───
def fmt(n):
    return f"{n:,.0f}"

def byd_fee(usd):
    if usd <= 10000:    return 1.0 * bhm
    elif usd <= 20000:  return 1.5 * bhm
    elif usd <= 40000:  return 2.5 * bhm
    elif usd <= 60000:  return 4.0 * bhm
    elif usd <= 100000: return 7.0 * bhm
    elif usd <= 200000: return 10.0 * bhm
    elif usd <= 500000: return 15.0 * bhm
    elif usd <= 1000000:return 20.0 * bhm
    else:               return 25.0 * bhm

def byd_label(usd):
    if usd <= 10000:    return "1 × BHM"
    elif usd <= 20000:  return "1.5 × BHM"
    elif usd <= 40000:  return "2.5 × BHM"
    elif usd <= 60000:  return "4 × BHM"
    elif usd <= 100000: return "7 × BHM"
    elif usd <= 200000: return "10 × BHM"
    elif usd <= 500000: return "15 × BHM"
    elif usd <= 1000000:return "20 × BHM"
    else:               return "25 × BHM"

# ════════════════════════════════════
# 1. ASOSIY MA'LUMOT
# ════════════════════════════════════
if menu == "🏠 Asosiy ma'lumot":
    st.markdown("## 📝 VM № 55 Qaror haqida")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='info-box'>
        <h4>🎯 Asosiy maqsad</h4>
        <ul>
        <li>Bojxona yig'imlarini JST talablariga moslashtirish</li>
        <li>Import va eksport yig'imlarini muvofiqlashtirish</li>
        <li>Hisoblash tizimini soddalashtirish</li>
        </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>✨ Asosiy o'zgarishlar</h4>
        <ul>
        <li>9 bosqichli stavkalar tizimi (BHM × 1 dan 25 gacha)</li>
        <li>Dastlabki deklaratsiyada 20% chegirma</li>
        <li>Ish vaqtidan tashqari uchun qo'shimcha to'lov</li>
        <li>Jismoniy shaxslar uchun alohida stavkalar</li>
        </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📌 Barcha yig'im turlari (VM № 55, 1-ilova)")
    rows = [
        ("1a","BYD — tovar qiymatiga qarab (import/eksport)","BHM × 1 dan 25 gacha"),
        ("1b","Tranzit / Qayta ishlash rejimi (1 deklaratsiya)","BHM × 25%"),
        ("1v","Naqd chet el valyutasi deklaratsiyasi (yuridik)","BHM × 2.5"),
        ("1g","Bojxona kirim orderi (1 dona)","BHM × 25%"),
        ("1d","Xalqaro kuryerlik jo'natmasi (1 kg brutto)","BHM × 2%"),
        ("2","BYDga o'zgartirish / qo'shimcha kiritish","BHM × 25%"),
        ("3a","Ish vaqtidan tashqari rasmiylashtiruv (1 BYD)","BHM × 25%"),
        ("3b-1","Bojxona ko'rigi — ish vaqtida (1 soat)","BHM × 25%"),
        ("3b-2","Bojxona ko'rigi — ish vaqtidan tashqari (1 soat)","BHM × 2"),
        ("4a","Bojxona ombori: 1-10 sutka (1 tonna/kun)","BHM × 3%"),
        ("4b","Bojxona ombori: 10+ sutka (1 tonna/kun)","BHM × 4%"),
        ("5a","Avtomobil hamrohligi: 200 km gacha","BHM × 2"),
        ("5b","Avtomobil hamrohligi: 200 km dan ortiq","BHM × 5"),
        ("6","Dastlabki qarorni qabul qilish","BHM × 75%"),
        ("7a","Chegara ombori: 1-5 kun (100 kg/kun)","BHM × 5%"),
        ("7b","Chegara ombori: 6-15 kun (100 kg/kun)","BHM × 7%"),
        ("7v","Chegara ombori: 15+ kun (100 kg/kun)","BHM × 10%"),
        ("7g","Tez buziladigan — chegara ombori (100 kg/kun)","BHM × 15%"),
        ("8","Tranzit deklaratsiyasiga o'zgartirish","BHM × 10%"),
        ("9","Intellektual mulk reyestriga kiritish (1 obyekt)","BHM × 1"),
    ]
    df = pd.DataFrame(rows, columns=["Modda", "Yig'im turi", "Stavka"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("🎁 **Dastlabki deklaratsiyalashda 1a-modda bo'yicha 20% chegirma beriladi!**")
    st.warning("⚠️ 1a-modda va 3-modda — 2026-yil 1-yanvardan kuchga kiradi. Qolganlari 2025-yil 1-maydan.")

# ════════════════════════════════════
# 2. RASMIYLASHTIRUV YIG'IMI
# ════════════════════════════════════
elif menu == "📋 Rasmiylashtiruv yig'imi":
    st.markdown("## 📋 BYD Rasmiylashtiruv Yig'imi Kalkulyatori")
    st.markdown("<div class='info-box'><b>1a-modda:</b> Tovarlarni import, eksport va boshqa bojxona rejimlarida BYD orqali rasmiylashtirganda (vaqtincha saqlash, davlat foydasiga voz kechish va yo'q qilishdan tashqari).</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        customs_usd = st.number_input("🔢 Tovarning bojxona qiymati (USD):", min_value=0.0, max_value=50000000.0, value=50000.0, step=1000.0, format="%.0f")
        st.caption(f"So'mda: **{fmt(customs_usd * USD_RATE)}** so'm")
        initial_decl = st.checkbox("✅ Dastlabki deklaratsiyalash (20% chegirma)")
        after_hours = st.checkbox("🌙 Ish vaqtidan tashqari rasmiylashtiruv (1 BYD, +BHM 25%)")
        insp_h = st.number_input("🔍 Ko'rig soatlari (ish vaqtida):", min_value=0, max_value=24, value=0)
        insp_ot = st.number_input("🔍 Ko'rig soatlari (ish vaqtidan tashqari):", min_value=0, max_value=24, value=0)
    with col2:
        tbl_data = {
            "Qiymat (USD)": ["≤10,000","≤20,000","≤40,000","≤60,000","≤100,000","≤200,000","≤500,000","≤1,000,000",">1,000,000"],
            "Stavka": ["1×BHM","1.5×BHM","2.5×BHM","4×BHM","7×BHM","10×BHM","15×BHM","20×BHM","25×BHM"],
        }
        st.dataframe(pd.DataFrame(tbl_data), hide_index=True, use_container_width=True)

    base = byd_fee(customs_usd)
    disc = base * 0.2 if initial_decl else 0.0
    ah_fee = 0.25 * bhm if after_hours else 0.0
    insp_fee = 0.25 * bhm * insp_h
    insp_ot_fee = 2.0 * bhm * insp_ot
    total = (base - disc) + ah_fee + insp_fee + insp_ot_fee

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Tovar qiymati", f"${fmt(customs_usd)}", f"{fmt(customs_usd * USD_RATE)} so'm")
    r2.metric(f"Asosiy yig'im ({byd_label(customs_usd)})", f"{fmt(base)} so'm", f"-{fmt(disc)} so'm" if initial_decl else "")
    r3.metric("Qo'shimcha to'lovlar", f"{fmt(ah_fee + insp_fee + insp_ot_fee)} so'm")
    r4.metric("💰 JAMI", f"{fmt(total)} so'm", f"${total/USD_RATE:.2f}")

    st.markdown(f"<div class='result-box'><h2 style='color:white;margin:0;'>Jami to'lov: {fmt(total)} so'm</h2><p style='margin:5px 0 0 0;opacity:0.85;'>≈ ${total/USD_RATE:.2f} · BHM={bhm:,} so'm · 1 USD={fmt(USD_RATE)} so'm</p></div>", unsafe_allow_html=True)

    with st.expander("📊 Batafsil hisoblash"):
        det = [("Bojxona qiymati", f"${fmt(customs_usd)}", f"{fmt(customs_usd*USD_RATE)} so'm"),
               (f"Asosiy yig'im ({byd_label(customs_usd)})", f"{fmt(base)} so'm", "")]
        if initial_decl: det.append(("✅ Dastlabki chegirma (−20%)", f"−{fmt(disc)} so'm", ""))
        if after_hours: det.append(("🌙 Ish vaqtidan tashqari (BHM 25%)", f"+{fmt(ah_fee)} so'm", ""))
        if insp_h > 0: det.append((f"🔍 Ko'rig ish vaqtida ({insp_h} soat × BHM 25%)", f"+{fmt(insp_fee)} so'm", ""))
        if insp_ot > 0: det.append((f"🔍 Ko'rig ish vaqtidan tashqari ({insp_ot} soat × BHM 2)", f"+{fmt(insp_ot_fee)} so'm", ""))
        det.append(("━━ JAMI", f"{fmt(total)} so'm", f"${total/USD_RATE:.2f}"))
        st.dataframe(pd.DataFrame(det, columns=["Qism","Miqdor","Izoh"]), hide_index=True, use_container_width=True)

# ════════════════════════════════════
# 3. TRANZIT VA MAXSUS REJIMLAR
# ════════════════════════════════════
elif menu == "🔄 Tranzit va maxsus rejimlar":
    st.markdown("## 🔄 Tranzit va Maxsus Rejimlar")
    tab1, tab2, tab3, tab4 = st.tabs(["🚛 Tranzit/Qayta ishlash","💵 Naqd valyuta","📄 Kirim orderi","📦 Kuryerlik"])

    with tab1:
        st.markdown("<div class='info-box'><b>1b-modda:</b> «tranzit», «bojxona hududida qayta ishlash», «bojxona hududidan tashqarida qayta ishlash» rejimlari.<br><b>Stavka: BHM × 25% — 1 deklaratsiya uchun</b></div>", unsafe_allow_html=True)
        n = st.number_input("Deklaratsiyalar soni:", min_value=1, max_value=1000, value=1, key="tr_n")
        ah = st.checkbox("Ish vaqtidan tashqari (+BHM 25% / BYD)", key="tr_ah")
        fee1 = 0.25 * bhm * n
        fee2 = 0.25 * bhm * n if ah else 0.0
        c1,c2,c3 = st.columns(3)
        c1.metric("Asosiy yig'im", f"{fmt(fee1)} so'm", f"{n} × BHM 25%")
        c2.metric("Ish vaqtidan tashqari", f"{fmt(fee2)} so'm")
        c3.metric("Jami", f"{fmt(fee1+fee2)} so'm", f"${(fee1+fee2)/USD_RATE:.2f}")

    with tab2:
        st.markdown("<div class='info-box'><b>1v-modda:</b> Yuridik shaxslar tomonidan olib kelinayotgan naqd chet el valyutasi.<br><b>Stavka: BHM × 2.5 — 1 deklaratsiya uchun</b></div>", unsafe_allow_html=True)
        n2 = st.number_input("Deklaratsiyalar soni:", min_value=1, max_value=100, value=1, key="cur_n")
        f2 = 2.5 * bhm * n2
        c1,c2 = st.columns(2)
        c1.metric("Yig'im", f"{fmt(f2)} so'm", f"{n2} × BHM 2.5")
        c2.metric("USD da", f"${f2/USD_RATE:.2f}")

    with tab3:
        st.markdown("<div class='info-box'><b>1g-modda:</b> Umumiy shakldagi bojxona kirim orderini qo'llash orqali.<br><b>Stavka: BHM × 25% — 1 kirim orderi uchun</b></div>", unsafe_allow_html=True)
        n3 = st.number_input("Kirim orderlari soni:", min_value=1, max_value=1000, value=1, key="ord_n")
        f3 = 0.25 * bhm * n3
        c1,c2 = st.columns(2)
        c1.metric("Yig'im", f"{fmt(f3)} so'm", f"{n3} × BHM 25%")
        c2.metric("USD da", f"${f3/USD_RATE:.2f}")

    with tab4:
        st.markdown("<div class='info-box'><b>1d-modda:</b> Xalqaro kuryerlik tashkilotining murojaatiga asosan xalqaro kuryerlik jo'natmalari.<br><b>Stavka: BHM × 2% — 1 kg brutto uchun</b></div>", unsafe_allow_html=True)
        kg = st.number_input("Og'irlik (kg brutto):", min_value=0.1, max_value=10000.0, value=1.0, step=0.1)
        f4 = 0.02 * bhm * kg
        c1,c2,c3 = st.columns(3)
        c1.metric("Og'irlik", f"{kg} kg")
        c2.metric("Yig'im", f"{fmt(f4)} so'm", f"{kg} × BHM 2%")
        c3.metric("USD da", f"${f4/USD_RATE:.2f}")

# ════════════════════════════════════
# 4. OMBOR SAQLASH
# ════════════════════════════════════
elif menu == "🏪 Ombor saqlash":
    st.markdown("## 🏪 Bojxona Omborida Saqlash Yig'imi")
    tab1, tab2 = st.tabs(["📦 Bojxona ombori (yuridik)","👤 Chegara ombori (jismoniy)"])

    with tab1:
        st.markdown("<div class='info-box'><b>4-modda:</b> Egasi bojxona organi bo'lgan bojxona ombori:<br>• Dastlabki 10 sutka: BHM × 3% / 1 tonna / sutka<br>• Har keyingi sutka: BHM × 4% / 1 tonna / sutka</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            w_t = st.number_input("Tovar og'irligi (tonna):", min_value=0.01, max_value=10000.0, value=1.0, step=0.1)
            days_t = st.number_input("Saqlash kunlari:", min_value=1, max_value=365, value=15)
        with col2:
            d1 = min(days_t, 10)
            d2 = max(0, days_t - 10)
            f_d1 = 0.03 * bhm * w_t * d1
            f_d2 = 0.04 * bhm * w_t * d2
            total_s = f_d1 + f_d2
            st.markdown(f"<div class='metric-card'><p>📅 1-10 kun: <b>{d1} kun</b> → {fmt(f_d1)} so'm</p><p>📅 10+ kun: <b>{d2} kun</b> → {fmt(f_d2)} so'm</p><hr><b>JAMI: {fmt(total_s)} so'm</b> (${total_s/USD_RATE:.2f})</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='info-box'><b>7-modda:</b> Jismoniy shaxslar — chegara bojxona postlari orqali notijorat maqsadlarda, me'yordan ortiq tovarlar:<br>• 1-5 kun: BHM × 5% / 100 kg / kun<br>• 6-15 kun: BHM × 7% / 100 kg / kun<br>• 15+ kun: BHM × 10% / 100 kg / kun<br>• Tez buziladigan: BHM × 15% / 100 kg / kun</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            w_kg = st.number_input("Tovar og'irligi (kg brutto):", min_value=1.0, max_value=100000.0, value=100.0, step=10.0)
            d_p = st.number_input("Saqlash kunlari:", min_value=1, max_value=180, value=10, key="phdays")
            perishable = st.checkbox("Tez buziladigan tovar")
        with col2:
            h100 = w_kg / 100.0
            if perishable:
                pf = 0.15 * bhm * h100 * d_p
                st.metric("Jami yig'im", f"{fmt(pf)} so'm", "BHM 15% / 100kg / kun")
            else:
                a1 = min(d_p, 5)
                a2 = min(max(0, d_p - 5), 10)
                a3 = max(0, d_p - 15)
                pf1 = 0.05 * bhm * h100 * a1
                pf2 = 0.07 * bhm * h100 * a2
                pf3 = 0.10 * bhm * h100 * a3
                pf = pf1 + pf2 + pf3
                rows = []
                if a1 > 0: rows.append(["1–5 kun", a1, "5%", fmt(pf1)])
                if a2 > 0: rows.append(["6–15 kun", a2, "7%", fmt(pf2)])
                if a3 > 0: rows.append(["15+ kun", a3, "10%", fmt(pf3)])
                st.dataframe(pd.DataFrame(rows, columns=["Davr","Kun","Stavka","So'm"]), hide_index=True, use_container_width=True)
                st.metric("JAMI", f"{fmt(pf)} so'm", f"${pf/USD_RATE:.2f}")

# ════════════════════════════════════
# 5. AVTOMOBIL HAMROHLIGI
# ════════════════════════════════════
elif menu == "🚗 Avtomobil hamrohligi":
    st.markdown("## 🚗 Avtotransport Hamrohligi Yig'imi")
    st.markdown("<div class='info-box'><b>5-modda:</b> O'zbekiston hududida bitta avtotransport vositasini bojxona hamrohligida kuzatib borganlik uchun:<br>• 200 km gacha: BHM × 2<br>• 200 km dan ortiq: BHM × 5</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        km = st.number_input("Masofa (km):", min_value=1, max_value=5000, value=150, step=10)
        vehicles = st.number_input("Avtomobil soni:", min_value=1, max_value=100, value=1)
    with col2:
        rate = 2.0 if km <= 200 else 5.0
        label = "BHM × 2 (200 km gacha)" if km <= 200 else "BHM × 5 (200 km dan ortiq)"
        fee_e = rate * bhm * vehicles
        st.markdown(f"<div class='result-box'><h3 style='color:white;margin:0;'>{label}</h3><h2 style='color:white;margin:10px 0;'>{fmt(fee_e)} so'm</h2><p style='margin:0;opacity:0.8;'>{vehicles} avtomobil · ${fee_e/USD_RATE:.2f}</p></div>", unsafe_allow_html=True)

    distances = list(range(50, 501, 50))
    esc_fees = [2*bhm if d<=200 else 5*bhm for d in distances]
    fig = go.Figure(go.Bar(
        x=distances, y=esc_fees,
        marker_color=['#2563eb' if d<=200 else '#dc2626' for d in distances],
        text=[fmt(f) for f in esc_fees], textposition='outside'
    ))
    fig.update_layout(title="Masofaga qarab hamrohlik yig'imi (1 avtomobil)", xaxis_title="Masofa (km)", yaxis_title="Yig'im (so'm)", template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════
# 6. JISMONIY SHAXSLAR
# ════════════════════════════════════
elif menu == "👤 Jismoniy shaxslar":
    st.markdown("## 👤 Jismoniy Shaxslar Uchun Yig'imlar")
    st.info("Chegara bojxona postlarida jismoniy shaxslar uchun alohida stavkalar qo'llaniladi.")
    tab1, tab2 = st.tabs(["📦 Chegara ombori saqlash","📋 Umumiy rasmiylashtiruv"])

    with tab1:
        st.markdown("<div class='info-box'><b>7-modda:</b> Notijorat maqsadlarda, belgilangan me'yordan ortiq bo'lgan tovarlar.</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            w = st.number_input("Og'irlik (kg brutto):", min_value=1.0, max_value=50000.0, value=100.0, key="ph2w")
            d = st.number_input("Saqlash kunlari:", min_value=1, max_value=180, value=7, key="ph2d")
            per2 = st.checkbox("Tez buziladigan", key="ph2p")
        with col2:
            h = w/100.0
            if per2:
                tf = 0.15*bhm*h*d
                st.metric("Jami yig'im", f"{fmt(tf)} so'm", "BHM 15%/100kg/kun")
            else:
                a1=min(d,5); a2=min(max(0,d-5),10); a3=max(0,d-15)
                f1=0.05*bhm*h*a1; f2=0.07*bhm*h*a2; f3=0.10*bhm*h*a3
                tf=f1+f2+f3
                rows=[]
                if a1>0: rows.append(["1–5 kun",a1,"5%",fmt(f1)])
                if a2>0: rows.append(["6–15 kun",a2,"7%",fmt(f2)])
                if a3>0: rows.append(["15+ kun",a3,"10%",fmt(f3)])
                st.dataframe(pd.DataFrame(rows,columns=["Davr","Kun","Stavka","So'm"]),hide_index=True,use_container_width=True)
                st.metric("JAMI", f"{fmt(tf)} so'm", f"${tf/USD_RATE:.2f}")

    with tab2:
        v = st.number_input("Tovar qiymati (USD):", min_value=0.0, max_value=1000000.0, value=5000.0, step=100.0, key="ph2v")
        init = st.checkbox("Dastlabki deklaratsiya (20% chegirma)", key="ph2i")
        bf = byd_fee(v) * (0.8 if init else 1.0)
        st.metric("Rasmiylashtiruv yig'imi", f"{fmt(bf)} so'm", byd_label(v)+(" · −20%" if init else ""))

# ════════════════════════════════════
# 7. BOSHQA XIZMATLAR
# ════════════════════════════════════
elif menu == "📜 Boshqa xizmatlar":
    st.markdown("## 📜 Boshqa Bojxona Xizmatlari")
    tab1, tab2, tab3, tab4 = st.tabs(["✏️ BYD O'zgartirish","⚖️ Dastlabki qaror","🔄 Tranzit o'zgartirish","🧠 Intellektual mulk"])

    with tab1:
        st.markdown("<div class='info-box'><b>2-modda:</b> Deklarant murojaatiga asosan BYDga o'zgartirish va/yoki qo'shimcha kiritish.<br>• Qog'oz: 1 dona BYD uchun; Elektron: 1 dona tuzatish shakli uchun<br><b>Stavka: BHM × 25%</b></div>", unsafe_allow_html=True)
        n = st.number_input("O'zgartirish soni:", min_value=1, max_value=1000, value=1, key="bch_n")
        f = 0.25*bhm*n
        c1,c2=st.columns(2); c1.metric("Yig'im",f"{fmt(f)} so'm",f"{n} × BHM 25%"); c2.metric("USD da",f"${f/USD_RATE:.2f}")

    with tab2:
        st.markdown("<div class='info-box'><b>6-modda:</b> Tovar bo'yicha dastlabki qarorni qabul qilish.<br><b>Stavka: BHM × 75%</b><br><i>Qaror bekor qilinsa yoki o'zgartirilsa to'lov qaytarilmaydi.</i></div>", unsafe_allow_html=True)
        n2 = st.number_input("Qarorlar soni:", min_value=1, max_value=100, value=1, key="pq_n")
        f2 = 0.75*bhm*n2
        c1,c2=st.columns(2); c1.metric("Yig'im",f"{fmt(f2)} so'm",f"{n2} × BHM 75%"); c2.metric("USD da",f"${f2/USD_RATE:.2f}")
        st.warning("⚠️ Qaror bekor qilinsa to'lov qaytarilmaydi!")

    with tab3:
        st.markdown("<div class='info-box'><b>8-modda:</b> Deklarantning murojaatiga asosan bojxona organi tomonidan tranzit deklaratsiyasiga o'zgartirish.<br>(Axborot tizimida deklaratsiyalovchi shaxs tomonidan o'zgartirishlar bundan mustasno)<br><b>Stavka: BHM × 10%</b></div>", unsafe_allow_html=True)
        n3 = st.number_input("O'zgartirish soni:", min_value=1, max_value=1000, value=1, key="tch_n")
        f3 = 0.10*bhm*n3
        c1,c2=st.columns(2); c1.metric("Yig'im",f"{fmt(f3)} so'm",f"{n3} × BHM 10%"); c2.metric("USD da",f"${f3/USD_RATE:.2f}")

    with tab4:
        st.markdown("<div class='info-box'><b>9-modda:</b> Bir intellektual mulk obyektini bojxona reyestriga kiritish.<br><b>Stavka: BHM × 1</b></div>", unsafe_allow_html=True)
        n4 = st.number_input("Obyektlar soni:", min_value=1, max_value=100, value=1, key="ip_n")
        f4 = 1.0*bhm*n4
        c1,c2=st.columns(2); c1.metric("Yig'im",f"{fmt(f4)} so'm",f"{n4} × BHM 1"); c2.metric("USD da",f"${f4/USD_RATE:.2f}")

# ════════════════════════════════════
# 8. BARCHA STAVKALAR JADVALI
# ════════════════════════════════════
elif menu == "📊 Barcha stavkalar jadvali":
    st.markdown("## 📊 Barcha Bojxona Yig'imlari Stavkalari Jadvali")
    st.caption(f"BHM = {bhm:,} so'm · 1 USD = {fmt(USD_RATE)} so'm")

    tab1, tab2 = st.tabs(["📦 BYD asosiy stavkalar","🔧 Barcha boshqa xizmatlar"])

    with tab1:
        rates = [1, 1.5, 2.5, 4, 7, 10, 15, 20, 25]
        main_d = {
            "Bojxona qiymati (USD)": ["≤10,000","≤20,000","≤40,000","≤60,000","≤100,000","≤200,000","≤500,000","≤1,000,000",">1,000,000"],
            "Stavka (BHM)": rates,
            "Yig'im (so'm)": [round(r*bhm) for r in rates],
            "Chegirmali -20% (so'm)": [round(r*bhm*0.8) for r in rates],
        }
        df1 = pd.DataFrame(main_d)
        st.dataframe(df1.style.format({"Yig'im (so'm)":"{:,.0f}","Chegirmali -20% (so'm)":"{:,.0f}"}), use_container_width=True, hide_index=True)
        st.success("✅ 'Chegirmali' ustun — dastlabki deklaratsiyalashda 20% chegirma qo'llanilganda")

    with tab2:
        sp_rates = [0.25,2.5,0.25,0.02,0.25,0.25,0.25,2.0,0.03,0.04,2.0,5.0,0.75,0.05,0.07,0.10,0.15,0.10,1.0]
        sp_d = {
            "Modda":["1b","1v","1g","1d","2","3a","3b-1","3b-2","4a","4b","5a","5b","6","7a","7b","7v","7g","8","9"],
            "Xizmat turi":[
                "Tranzit/Qayta ishlash (1 deklaratsiya)","Naqd valyuta deklaratsiyasi (yuridik)",
                "Bojxona kirim orderi (1 dona)","Xalqaro kuryerlik (1 kg brutto)",
                "BYD o'zgartirish/qo'shimcha (1 dona)","Ish vaqtidan tashqari rasmiylashtiruv (1 BYD)",
                "Bojxona ko'rigi — ish vaqtida (1 soat)","Bojxona ko'rigi — ish vaqtidan tashqari (1 soat)",
                "Ombor: 1-10 sutka (1 tonna/kun)","Ombor: 10+ sutka (1 tonna/kun)",
                "Avtomobil hamrohligi: 200 km gacha","Avtomobil hamrohligi: 200 km dan ortiq",
                "Dastlabki qarorni qabul qilish","Chegara ombori: 1-5 kun (100 kg/kun)",
                "Chegara ombori: 6-15 kun (100 kg/kun)","Chegara ombori: 15+ kun (100 kg/kun)",
                "Tez buziladigan — chegara ombori (100 kg/kun)","Tranzit deklaratsiyasiga o'zgartirish",
                "Intellektual mulk reyestriga kiritish (1 obyekt)"
            ],
            "Stavka":["BHM 25%","BHM 2.5×","BHM 25%","BHM 2%","BHM 25%","BHM 25%","BHM 25%","BHM 2×","BHM 3%","BHM 4%","BHM 2×","BHM 5×","BHM 75%","BHM 5%","BHM 7%","BHM 10%","BHM 15%","BHM 10%","BHM 1×"],
            "Yig'im (so'm)":[round(r*bhm) for r in sp_rates],
        }
        df2 = pd.DataFrame(sp_d)
        st.dataframe(df2.style.format({"Yig'im (so'm)":"{:,.0f}"}), use_container_width=True, hide_index=True)
        st.caption(f"Barcha miqdorlar BHM = {bhm:,} so'm asosida hisoblangan")

# ════════════════════════════════════
# 9. GRAFIK TAHLIL
# ════════════════════════════════════
elif menu == "📈 Grafik tahlil":
    st.markdown("## 📈 Grafik Tahlil")
    st.caption(f"BHM = {bhm:,} so'm · 1 USD = {fmt(USD_RATE)} so'm")

    col1, col2 = st.columns(2)
    with col1:
        vals = [5000,15000,30000,50000,80000,150000,350000,750000,1500000]
        fees_n = [byd_fee(v) for v in vals]
        fees_d = [byd_fee(v)*0.8 for v in vals]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=vals,y=fees_n,mode='lines+markers',name="Oddiy",line=dict(color='#2563eb',width=3),marker=dict(size=9)))
        fig1.add_trace(go.Scatter(x=vals,y=fees_d,mode='lines+markers',name="Dastlabki (−20%)",line=dict(color='#10b981',width=2,dash='dash'),marker=dict(size=8)))
        fig1.update_layout(title="BYD Rasmiylashtiruv Yig'imi",xaxis_title="Tovar qiymati (USD)",yaxis_title="Yig'im (so'm)",template='plotly_white',hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        svcs = ["Tranzit","Valyuta","Kirim orderi","Kuryer(1kg)","BYD o'zg.","Ish tashq.","Ko'rig(ish)","Ko'rig(tash.)","Avto 200km-","Avto 200km+","Dastl. qaror","Intel. mulk"]
        sfees = [0.25*bhm,2.5*bhm,0.25*bhm,0.02*bhm,0.25*bhm,0.25*bhm,0.25*bhm,2*bhm,2*bhm,5*bhm,0.75*bhm,bhm]
        fig2 = go.Figure(go.Bar(x=svcs,y=sfees,marker_color='#2563eb',text=[fmt(f) for f in sfees],textposition='outside',textfont=dict(size=9)))
        fig2.update_layout(title="Maxsus Xizmatlar Yig'imi",yaxis_title="Yig'im (so'm)",template='plotly_white',xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🏪 Omborda Saqlash Xarajati (1 tonna, kunlar bo'yicha)")
    drange = list(range(1,31))
    sfees2 = [min(d,10)*0.03*bhm + max(0,d-10)*0.04*bhm for d in drange]
    fig3 = go.Figure(go.Scatter(x=drange,y=sfees2,mode='lines+markers',fill='tozeroy',line=dict(color='#7c3aed',width=2),marker=dict(size=7)))
    fig3.add_vline(x=10,line_dash="dash",line_color="red",annotation_text="10-kun chegara")
    fig3.update_layout(title="Ombor saqlash jami xarajati (1 tonna, 1–30 kun)",xaxis_title="Kunlar soni",yaxis_title="Jami xarajat (so'm)",template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)

# ─── FOOTER ───
st.divider()
col1,col2,col3 = st.columns(3)
with col1: st.info("📞 Bojxona qo'mitasi: **1155**\n\n📧 info@customs.uz")
with col2: st.success("🌐 my.customs.uz\n\n📋 lex.uz")
with col3: st.warning(f"📅 Kurs: {usd_date}\n\n💰 BHM: {bhm:,} so'm")
st.markdown(f"""<div style='text-align:center;color:#888;padding:15px;font-size:13px;'>
© 2025 Bojxona Yig'imlari Kalkulyatori · VM № 55 · 31.01.2025<br>
BHM = {bhm:,} so'm · 1 USD = {fmt(USD_RATE)} so'm (CBU)<br>
<small>Faqat ma'lumot berish maqsadida. Rasmiy hujjatlar bilan taqqoslang.</small>
</div>""", unsafe_allow_html=True)
