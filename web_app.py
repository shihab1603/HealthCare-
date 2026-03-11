import streamlit as st
import pandas as pd
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="HealthCare", layout="centered")

# ২. কাস্টম সিএসএস
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stNumberInput, .stTextInput { border-radius: 10px; }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 HealthCare Smart Suggestion")

# ৩. ইনপুট সেকশন
with st.expander("📝 আপনার প্রোফাইল পূরণ করুন", expanded=True):
    name = st.text_input("আপনার নাম", placeholder="আপনার নাম লিখুন")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("বয়স (Age)",  value=0)
        feet = st.number_input("উচ্চতা (ফুট)",value=0)
    with col2:
        weight = st.number_input("ওজন (কেজি)",value=0)
        inches = st.number_input("উচ্চতা (ইঞ্চি)", value=0)

# ৪. ডাটা লোড
try:
    df = pd.read_excel("Health.xlsx")
    df.columns = df.columns.str.strip()
except Exception:
    st.error("❗ 'Health.xlsx' ফাইলটি পাওয়া যায়নি।")
    st.stop()

# ৫. রেঞ্জ চেক ফাংশন
def check_range(val, range_str):
    try:
        range_str = str(range_str).strip()
        if '-' in range_str:
            low, high = map(float, range_str.split('-'))
            return low <= val <= high
        return float(range_str) == val
    except: return False

# ৬. ক্যালকুলেশন এবং রেজাল্ট
if st.button("ফলাফল দেখুন"):
    with st.spinner('আপনার জন্য সেরা রুটিন তৈরি হচ্ছে...'):
        time.sleep(1)
        
        # BMI ক্যালকুলেশন
        height_m = ((feet * 12) + inches) * 0.0254
        bmi = round(weight / (height_m ** 2), 1)

        # স্ট্যাটাস নির্ধারণ
        if bmi < 18.5: status, color, advice = "Underweight", "#FFA726", "আপনার পুষ্টিকর খাবার বাড়ানো প্রয়োজন।"
        elif 18.5 <= bmi <= 24.9: status, color, advice = "Normal", "#2ECC71", "চমৎকার! আপনি একদম ফিট আছেন।"
        elif 25.0 <= bmi <= 29.9: status, color, advice = "Overweight", "#E67E22", "একটু সচেতন হওয়া এবং ব্যায়াম করা প্রয়োজন।"
        else: status, color, advice = "Obese", "#E74C3C", "দ্রুত ডায়েট কন্ট্রোল এবং বিশেষজ্ঞের পরামর্শ নিন।"

        
        # BMI রেজাল্ট কার্ড
        st.markdown(f"""
            <div style="background-color:{color};" class="status-card">
                <h2 style="margin:0;">{status} (BMI: {bmi})</h2>
                <p style="margin:0; opacity:0.9;">{advice}</p>
            </div>
            """, unsafe_allow_html=True)

        # ডাটা ম্যাচিং
        matched = df[df.apply(lambda r: check_range(age, r['Age']) and check_range(weight, r['Weight']), axis=1)]

        if not matched.empty:
            row = matched.iloc[0]
            st.markdown(f"### 📅 {name} এর জন্য বিশেষ পরামর্শ:")
            
            # খাবার এবং রুটিনকে টেবিল আকারে সাজানো
            food_list = str(row['Suggested Foods']).split(',') if pd.notna(row['Suggested Foods']) else []
            routine_list = str(row['Daily Routine']).replace('–', ',').split(',') if pd.notna(row['Daily Routine']) else []
            
            max_len = max(len(food_list), len(routine_list))
            food_list += [""] * (max_len - len(food_list))
            routine_list += [""] * (max_len - len(routine_list))

            # ফাইনাল টেবিল ডাটাফ্রেম
            final_table = pd.DataFrame({
                "Daily Routine (রুটিন)": [r.strip() for r in routine_list],
                "Suggested Foods (খাবার)": [f.strip() for f in food_list]
            })

            # st.dataframe ব্যবহার করলে Zoom, Download,অপশন অটোমেটিক চলে আসে
            st.dataframe(final_table, use_container_width=True, hide_index=True)
            
        else:
            st.warning("⚠️ আপনার এই বয়স ও ওজনের জন্য নির্দিষ্ট কোনো রুটিন আমাদের ডাটাবেসে নেই।")

st.markdown("---")
st.caption("Developed by Safetaka.com")