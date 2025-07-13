import streamlit as st
import pandas as pd
import joblib
import base64
import os

st.set_page_config(page_title="💳 Fraud Detector Pro", layout="centered", page_icon="🗫️")


model = joblib.load("fraud_detection_pipline_main_main2_33_pipeline_xgb1.pkl")


# ========= Enhanced CSS with animated fancy background =========
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #1e3c72, #2a5298);
    background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
    background-attachment: fixed;
    background-size: cover;
    font-family: 'Segoe UI', sans-serif;
    color: #f0f0f0;
    overflow-x: hidden;
}

.stApp {
    background: linear-gradient(135deg, rgba(29, 53, 87, 0.95), rgba(69, 123, 157, 0.95)),
                url("https://www.transparenttextures.com/patterns/cubes.png");
    background-size: cover;
    background-attachment: fixed;
    background-repeat: repeat;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
}

@keyframes glow {
    0% { box-shadow: 0 0 5px #fff; }
    50% { box-shadow: 0 0 20px #ff6ec4, 0 0 30px #ff6ec4; }
    100% { box-shadow: 0 0 5px #fff; }
}

.stApp > header, .stApp > footer {visibility: hidden;}

h1, h3, .stMarkdown p {
    color: #f0f0f0 !important;
    text-align: center;
}

.stButton > button {
    border-radius: 15px;
    background: linear-gradient(135deg, #fc466b, #3f5efb);
    color: white;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: bold;
    animation: glow 2s infinite;
    border: none;
    transition: 0.3s;
    text-shadow: 1px 1px 2px #000;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3f5efb, #fc466b);
    transform: scale(1.1);
    cursor: pointer;
}

section[data-testid="stSidebar"] > div:first-child {
    background-color: #1c1c2b;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
}

input, textarea, .stTextInput > div > div > input {
    background-color: #2f3542 !important;
    color: #f1f2f6 !important;
    border: none;
    border-radius: 10px;
    padding: 0.5rem;
    font-size: 16px;
}

.css-1cpxqw2 {
    background-color: #2f3542 !important;
    color: white;
}

/* Developer credit styling */
.dev-credit {
    background: rgba(0,0,0,0.6);
    padding: 12px 24px;
    border-radius: 12px;
    margin-top: 40px;
    box-shadow: 0 4px 15px rgba(255,255,255,0.2);
    text-align: center;
}
.dev-credit a {
    color: #ffffff;
    font-weight: bold;
    font-size: 18px;
    text-decoration: none;
    display: inline-block;
    margin-top: 5px;
    text-shadow: 0 0 8px #00c3ff;
}
</style>
""", unsafe_allow_html=True)

# ========= Header =========
st.markdown("<h1 style='font-size: 42px;'>🔐 Smart Fraud Detection System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 30px;'>🔍 Enter transaction details and check its authenticity</h3>", unsafe_allow_html=True)

# ========= User Input =========
col1, col2 = st.columns(2)
with col1:
    transaction_type = st.selectbox('Transaction Type', ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEPOSIT'], key="type")
    amount = st.number_input("Amount (₹)", min_value=0.0, value=1000.0)
with col2:
    oldbalanceOrg = st.number_input('Old Balance (Sender)', min_value=0.0, value=10000.0)
    newbalanceOrig = st.number_input('New Balance (Sender)', min_value=0.0, value=9000.0)

oldbalanceDest = st.number_input('Old Balance (Receiver)', min_value=0.0, value=0.0)
newbalanceDest = st.number_input('New Balance (Receiver)', min_value=0.0, value=0.0)

# ========= Prediction =========
if st.button('🔮 Predict Transaction'):
    raw_data = pd.DataFrame([{
        'type': transaction_type,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest
    }])
    prediction = model.predict(raw_data)[0]
    prob = model.predict_proba(raw_data)[0][1]
    st.markdown("<hr>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown("""
        <div style="background-color:#ff4d4d; padding:20px; border-radius:12px; animation: glow 2s infinite alternate;">
            <h3 style="color:white;">🚨 Fraudulent Transaction Detected!</h3>
            <p style="font-size:18px; color:white;">⚠ Probability: <b>{:.2%}</b></p>
        </div>
        """.format(prob), unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div style="background-color:#28a745; padding:20px; border-radius:12px; animation: glow 2s infinite alternate;">
            <h3 style="color:white;">✅ Transaction is Safe</h3>
            <p style="font-size:18px; color:white;">🔐 Probability: <b>{:.2%}</b></p>
        </div>
        """.format(1 - prob), unsafe_allow_html=True)
        st.snow()

# ========= Developer Credit =========
st.markdown("""
<div class="dev-credit">
    <a>👨‍💻 Developed by Razee Abdullaha Shaikh</a>
</div>
""", unsafe_allow_html=True)

# ========= PDF & Slides Viewer =========
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📂 View Project Outputs")

if "viewing_section" not in st.session_state:
    st.session_state.viewing_section = None
if "current_slide_index" not in st.session_state:
    st.session_state.current_slide_index = 0

powerbi_pdf_path = "Fraud_Detection-Razee Shaikh_PoweBI.pdf"

def display_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="650px" type="application/pdf"></iframe>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"❌ Unable to load PDF: {e}")

def display_slide_viewer():
    slides_folder = "slides"
    if not os.path.exists(slides_folder):
        st.error("❌ 'slides' folder not found.")
        return

    slide_images = sorted([img for img in os.listdir(slides_folder) if img.lower().endswith(('.jpg', '.png'))])
    total = len(slide_images)

    if total == 0:
        st.warning("⚠ No images found in slides folder.")
        return

    index = st.session_state.current_slide_index
    image_path = os.path.join(slides_folder, slide_images[index])
    st.image(image_path, caption=f"Slide {index + 1} of {total}", use_container_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", key="prev") and index > 0:
            st.session_state.current_slide_index -= 1
    with col2:
        st.markdown(f"<p style='text-align:center;'>Slide {index + 1} of {total}</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Next ➡️", key="next") and index < total - 1:
            st.session_state.current_slide_index += 1

# Viewer Buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.viewing_section is None and st.button("🖼 View Presentation Slides"):
        st.session_state.viewing_section = "slides"
with col2:
    if st.session_state.viewing_section is None and st.button("📈 View Power BI PDF"):
        st.session_state.viewing_section = "powerbi"

if st.session_state.viewing_section == "slides":
    st.subheader("🖼 Presentation Slides")
    display_slide_viewer()
    if st.button("❌ Close Slides View"):
        st.session_state.viewing_section = None
        st.session_state.current_slide_index = 0
elif st.session_state.viewing_section == "powerbi":
    st.subheader("📈 Power BI PDF")
    display_pdf(powerbi_pdf_path)
    if st.button("❌ Close Power BI View"):
        st.session_state.viewing_section = None
