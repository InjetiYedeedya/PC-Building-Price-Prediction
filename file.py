import streamlit as st
import pandas as pd
import joblib
import re

# ======================================
# Load model + dataset for dropdowns
# ======================================
model = joblib.load(r"C:\Users\yedee\Desktop\Streamlit\xgb_model_pipeline.pkl")
df = pd.read_csv(r"C:\Users\yedee\Desktop\Streamlit\my_data.csv")

# ======================================
# 🎨 L C S Branding + Header (Title + Logo + Tagline)
# ======================================

# Gold Title Centered
st.markdown("""
<h1 style='text-align: center; color: #D4AF37; font-size: 42px;'>
💻 L C S - Laptop Care Solutions
</h1>
""", unsafe_allow_html=True)

# Logo Left + Tagline Right
col1, col2 = st.columns([1, 3])

with col1:
    st.image(r"C:\Users\yedee\Desktop\Streamlit\IMG_20251116_165353_315.jpg", width=150)

with col2:
    st.markdown("""
    <div style='font-size:22px; margin-top:35px; color:#CCCCCC;'>
    <b>Your trusted destination for PC building, repair,<br>
    customization & system upgrades.</b>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# Helper Functions
# ======================================
def extract_number(text):
    match = re.search(r"(\d{3,5})", text)
    return float(match.group(1)) if match else 0

def get_gpu_family(model_name):
    match = re.search(r"(rtx|gtx|rx)", model_name)
    return match.group(1) if match else "other"

def get_storage_score(x):
    return {"ssd_nvme": 3, "ssd_sata": 2, "hdd": 1}.get(x, 1)

def opts(col):
    return sorted(df[col].unique())

# ======================================
# ✨ Special Offer (Coupon)
# ======================================
st.markdown("""
<div style='background-color:#2A2A2A; padding:15px; border-radius:10px; border-left: 8px solid #D4AF37; margin-top:20px;'>
<h3 style='color:#D4AF37;'>🎁 Special Offer – Zero Assembly Charges!</h3>
Use coupon code <b style='color:#FFD700;'>FREEASSEMBLY</b> and enjoy <b>complete PC assembly at no extra cost.</b><br>
Valid exclusively at <b>LCS</b>.
</div>
""", unsafe_allow_html=True)

# ======================================
# PC Configuration UI
# ======================================
st.header("🛠 Please enter your PC Configurations")

# 17 RAW columns
motherboard_brand = st.selectbox("Motherboard Brand", opts("motherboard_brand"))
#motherboard_chipset = st.selectbox("Motherboard Chipset", opts("motherboard_chipset"))

#cpu_brand = st.selectbox("CPU Brand", opts("cpu_brand"))
cpu_model = st.selectbox("CPU Model", opts("cpu_model"))

ram_brand = st.selectbox("RAM Brand", opts("ram_brand"))
ram_size_gb = st.selectbox("RAM Size", opts("ram_size_gb"))
ram_type = st.selectbox("RAM Type", opts("ram_type"))
ram_mhz = st.selectbox("RAM MHZ", opts("ram_speed_mhz"))

gpu_brand = st.selectbox("GPU Brand", opts("gpu_brand"))
gpu_model = st.selectbox("GPU Model", opts("gpu_model"))

cooler_brand = st.selectbox("Cooler Brand", opts("cooler_brand"))
cooler_type = st.selectbox("Cooler Type", opts("cooler_type"))

cabinet_brand = st.selectbox("Cabinet Brand", opts("cabinet_brand"))
cabinet_type = st.selectbox("Cabinet Type", opts("cabinet_type"))

psu_brand = st.selectbox("PSU Brand", opts("psu_brand"))
psu_wattage = st.selectbox("PSU Wattage", opts("psu_wattage"))

storage_type = st.selectbox("Storage Type", opts("storage_type"))
storage_capacity_gb = st.selectbox("Storage Capacity", opts("storage_capacity_gb"))

# ======================================
# Feature Engineering
# ======================================
ram_size_num = int(ram_size_gb.replace("_gb", ""))
storage_gb_num = int(storage_capacity_gb.replace("_gb", ""))
psu_watt_num = int(psu_wattage.replace("_wattage", ""))

cpu_number = extract_number(cpu_model)
gpu_number = extract_number(gpu_model)

gpu_family = get_gpu_family(gpu_model)
storage_type_score = get_storage_score(storage_type)

# ======================================
# FINAL INPUT DATAFRAME
# ======================================
input_data = pd.DataFrame([{
    "motherboard_brand": motherboard_brand,
    #"motherboard_chipset": motherboard_chipset,
    #"cpu_brand": cpu_brand,
    "cpu_model": cpu_model,
    "ram_brand": ram_brand,
    "ram_size_gb": ram_size_gb,
    "ram_type": ram_type,
    "ram_speed_mhz": ram_mhz, 
    "gpu_brand": gpu_brand,
    "gpu_model": gpu_model,
    "cooler_brand": cooler_brand,
    "cooler_type": cooler_type,
    "cabinet_brand": cabinet_brand,
    "cabinet_type": cabinet_type,
    "psu_brand": psu_brand,
    "psu_wattage": psu_wattage,
    "storage_type": storage_type,
    "storage_capacity_gb": storage_capacity_gb,

    # Engineered
    "ram_size_num": ram_size_num,
    "storage_gb_num": storage_gb_num,
    "psu_watt_num": psu_watt_num,
    "cpu_number": cpu_number,
    "gpu_number": gpu_number,
    "gpu_family": gpu_family,
    "storage_type_score": storage_type_score,
}])

st.subheader("🔍 Final Input Data Sent to Model")
st.dataframe(input_data)

# ======================================
# Prediction
# ======================================
if st.button("Predict Price"):
    price = model.predict(input_data)[0]
    st.success(f"💰 Estimated PC Price: ₹ {int(price):,}")

# ======================================
# 📞 CONTACT INFORMATION (Dark Theme)
# ======================================
st.markdown("""
<br>
<h3 style='color:#D4AF37;'>📞 For More Information</h3>

<div style='font-size:20px;'>
<b style='color:#444444;'>K. Pavan Kumar</b> – 
<span style='color:#8B0000; font-weight:bold;'>9030537325</span><br><br>

<b style='color:#444444;'>I. Yedeedya</b> – 
<span style='color:#8B0000; font-weight:bold;'>7286096262</span>
</div>
""", unsafe_allow_html=True)

# ======================================
# 🛠 DEVELOPER CREDITS (Dark Theme)
# ======================================
st.markdown("""
<br>
<div style='text-align:center; padding:12px; background-color:#111111; border-radius:10px;'>
<span style='color:#AAAAAA; font-size:16px;'>
Designed & Developed by <b style='color:#CCCCCC;'>Yedeedya Injeti</b><br>
Under <b style='color:#B8860B;'>Innomatics Research Labs</b>
</span>
</div>
<br>
""", unsafe_allow_html=True)

# base) C:\Users\yedee\Desktop\Streamlit>streamlit_env\Scripts\activate

# (streamlit_env) (base) C:\Users\yedee\Desktop\Streamlit>streamlit run file.py