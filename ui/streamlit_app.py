import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agents import DiagnosisAgent, RecommendationAgent
from core.model_loader import load_model

st.set_page_config(page_title="Pemantauan Kesehatan Pribadi", page_icon="🧠")
st.title("🧠 Pemantauan Kesehatan Pribadi (AI Multi-Agen)")

@st.cache_resource
def load_all_models():
    return {
        "diabetes": DiagnosisAgent(load_model("models/diabetes_logreg_model.pkl")),
        "heart": DiagnosisAgent(load_model("models/heart_logreg_model.pkl")),
        "stroke": DiagnosisAgent(load_model("models/stroke_logreg_model.pkl")),
    }

models = load_all_models()

# Initialize session state for diagnosis results if not exist
for disease in ["diabetes", "heart", "stroke"]:
    if disease not in st.session_state:
        st.session_state[disease] = None

# ======================= SECTION: Diabetes Diagnosis =========================
st.header("📥 Data Diabetes")
col1, col2 = st.columns(2)
with col1:
    pregnancies = st.number_input("Jumlah Kehamilan", min_value=0, step=1)
    st.caption("Jumlah kehamilan yang pernah dialami oleh pasien.")
    glucose = st.number_input("Glukosa", min_value=0.0, step=0.1)
    st.caption("Kadar glukosa dalam darah, penting untuk diagnosis diabetes.")
with col2:
    bmi = st.number_input("BMI", min_value=0.0, step=0.1)
    st.caption("Indeks massa tubuh (Body Mass Index) pasien.")
    age = st.number_input("Usia", min_value=0, step=1)
    st.caption("Usia pasien dalam tahun.")

if st.button("Diagnosa Diabetes"):
    features = [pregnancies, glucose, bmi, age]
    pred = models["diabetes"].predict(features)
    st.session_state["diabetes"] = bool(pred)

if st.session_state["diabetes"] is not None:
    status = "Positif ❌" if st.session_state["diabetes"] else "Negatif ✅"
    st.success(f"Hasil Diagnosis Diabetes: {status}")

# ======================= SECTION: Heart Diagnosis ============================
st.header("❤️ Data Jantung")
col1, col2 = st.columns(2)
with col1:
    cp = st.number_input("Tipe Nyeri Dada [0-3]", min_value=0, max_value=3, step=1)
    st.caption("Jenis nyeri dada: 0=tidak, 1=typical angina, 2=atypical angina, 3=non-anginal.")
    thalach = st.number_input("Detak Jantung Maksimum", min_value=0, step=1)
    st.caption("Detak jantung maksimum yang dicapai selama tes.")
with col2:
    oldpeak = st.number_input("Oldpeak", step=0.1)
    st.caption("Depresi ST akibat olahraga dibandingkan saat istirahat.")
    ca = st.number_input("Jumlah Arteri Tersumbat [0-4]", min_value=0, max_value=4, step=1)
    st.caption("Jumlah pembuluh arteri utama yang tersumbat (0-4).")

if st.button("Diagnosa Jantung"):
    features = [cp, thalach, oldpeak, ca]
    pred = models["heart"].predict(features)
    st.session_state["heart"] = bool(pred)

if st.session_state["heart"] is not None:
    status = "Positif ❌" if st.session_state["heart"] else "Negatif ✅"
    st.success(f"Hasil Diagnosis Jantung: {status}")

# ======================= SECTION: Stroke Diagnosis ===========================
st.header("🧠 Data Stroke")
col1, col2 = st.columns(2)
with col1:
    high_bp = st.selectbox("Hipertensi", options=[0, 1])
    st.caption("Hipertensi: 0 = tidak, 1 = ya (faktor risiko utama stroke).")
    chest_discomfort = st.selectbox("Nyeri Dada saat Aktivitas", options=[0, 1])
    st.caption("Adakah nyeri dada saat aktivitas? 0 = tidak, 1 = ya.")
with col2:
    irregular_heartbeat = st.selectbox("Detak Jantung Tidak Teratur", options=[0, 1])
    st.caption("Apakah detak jantung tidak teratur? 0 = tidak, 1 = ya.")
    stroke_risk = st.number_input("Risiko Stroke (%)", min_value=0.0, max_value=100.0, step=0.1)
    st.caption("Estimasi risiko stroke dalam persen berdasarkan gejala dan data medis.")

if st.button("Diagnosa Stroke"):
    features = [high_bp, chest_discomfort, irregular_heartbeat, stroke_risk]
    pred = models["stroke"].predict(features)
    st.session_state["stroke"] = bool(pred)

if st.session_state["stroke"] is not None:
    status = "Positif ❌" if st.session_state["stroke"] else "Negatif ✅"
    st.success(f"Hasil Diagnosis Stroke: {status}")

# ======================= SECTION: Rekomendasi AI Otomatis ====================
if all(st.session_state[disease] is not None for disease in ["diabetes", "heart", "stroke"]):
    st.markdown("---")
    st.header("💡 Rekomendasi Medis AI Berdasarkan Diagnosis")

    try:
        context = {
            "diabetes": st.session_state["diabetes"],
            "heart": st.session_state["heart"],
            "stroke": st.session_state["stroke"],
        }
        rec_agent = RecommendationAgent()
        rec_text = rec_agent.recommend(context)
        st.success(rec_text)
    except Exception as e:
        st.error(f"Gagal mendapatkan rekomendasi AI: {e}")
else:
    st.info("Lakukan diagnosis pada semua penyakit terlebih dahulu untuk mendapatkan rekomendasi AI.")