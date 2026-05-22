import streamlit as st # ไลบรารีสำหรับสร้าง Web Application
import pandas as pd # ไลบรารีสำหรับจัดการข้อมูลในรูปแบบ DataFrame
import numpy as np # ไลบรารีสำหรับคำนวณทางคณิตศาสตร์
import matplotlib.pyplot as plt # ไลบรารีสำหรับสร้างกราฟ
import seaborn as sns # ไลบรารีสำหรับสร้างกราฟที่สวยงามขึ้น
from scipy.stats.mstats import winsorize # ฟังก์ชันสำหรับจัดการ Outlier (Winsorization)
import io # ไลบรารีสำหรับจัดการ Input/Output
import warnings # ไลบรารีสำหรับจัดการคำเตือน
warnings.filterwarnings('ignore') # ไม่แสดงคำเตือน

# ตั้งค่า Streamlit page
st.set_page_config(layout="wide", page_title="Super Cute Data Cleaning App")

# --- Streamlit App Title ---
st.title("✨💖 Super Cute Data Cleaning Web App 💖✨") # ตั้งชื่อแอปพลิเคชัน
st.markdown("--- 🎀 ยินดีต้อนรับสู่แอปพลิเคชัน Data Cleaning แสนน่ารักของเรา! 🎀 ---") # ข้อความต้อนรับ
st.markdown("--- 🌟 ท่านสามารถอัปโหลดไฟล์ CSV และเลือกขั้นตอนการทำความสะอาดข้อมูลได้เลย! 🌟 ---") # คำแนะนำเบื้องต้น
st.error("⚠️ ใช้สำหรับชุดข้อมูลที่มีโครงสร้างคล้าย redbull_workshop_dirty.csv เท่านั้นนะ! ⚠️")

# --- File Uploader ---
uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV ของคุณที่นี่! 📂", type=["csv"])

# --- Data Cleaning Steps (as functions) ---

def perform_data_exploration(data):
    st.subheader("📊 1. สำรวจข้อมูลแสนสนุก! ✨")
    st.write("#### รูปทรงข้อมูลสุดปัง: 💪")
    st.write(f"มี {data.shape[0]:,} แถว และ {data.shape[1]} คอลัมน์")
    st.write("#### ข้อมูลเจาะลึก: 🕵️‍♀️")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())
    st.write("#### สถิติเชิงพรรณนา (คร่าวๆ): 📝")
    st.dataframe(data.describe(include='all'))
    return data

def handle_duplicate_data(data):
    st.subheader("👥 2. จัดการข้อมูลซ้ำซ้อน! 👯")
    exact_dups = data.duplicated()
    exact_dup_count = exact_dups.sum()
    if exact_dup_count > 0:
        st.warning(f"พบข้อมูลซ้ำ 100% จำนวน {exact_dup_count:,} แถว 😮‍💨")
        st.dataframe(data[exact_dups])
        data = data.drop_duplicates()
        st.success(f"✅ ลบข้อมูลซ้ำแล้ว! ตอนนี้เหลือ {len(data):,} แถว ✨")
    else:
        st.info("ไม่พบข้อมูลซ้ำซ้อนเลย! ข้อมูลของคุณเป๊ะปังมาก! 💯")
    return data

def handle_inconsistent_data(data):
    st.subheader("🔄 3. แก้ไขข้อมูลที่ไม่สอดคล้องกัน! 🧩")
    st.write("##### 🧐 ก่อนปรับปรุงค่าที่ไม่สอดคล้องกัน (ค่าที่ไม่ซ้ำกันในคอลัมน์หมวดหมู่)")
    cat_cols = ['Region', 'Product_Variant', 'Channel']
    for col in cat_cols:
        unique_vals = data[col].unique()
        st.write(f"**📌 {col} ({len(unique_vals)} ค่า):**")
        st.write(unique_vals)

    st.write("##### กำลังแก้ไขค่าที่ไม่สอดคล้องกัน... รอแป๊บนะ! ⏳")

    data['Region'] = data['Region'].str.strip().str.lower()
    region_mapping = {
        'th-central': 'TH-Central', 'th central': 'TH-Central',
        'thailand central': 'TH-Central', 'thailand-central': 'TH-Central',
        'thailand': 'TH-Central',
        'usa-east': 'USA-East', 'us east': 'USA-East',
        'united states east': 'USA-East', 'u.s.a.': 'USA-East',
        'europe-eu': 'Europe-EU', 'eu': 'Europe-EU',
        'europe': 'Europe-EU', 'european union': 'Europe-EU',
        'asia-pacific': 'Asia-Pacific', 'asia-pac': 'Asia-Pacific',
        'apac': 'Asia-Pacific', 'asia pacific': 'Asia-Pacific'
    }
    data['Region'] = data['Region'].replace(region_mapping)
    data['Region'] = data['Region'].str.upper()

    data['Product_Variant'] = data['Product_Variant'].str.strip().str.lower()
    product_variant_mapping = {
        'original blue': 'Original Blue', 'original  blue': 'Original Blue',
        'krating daeng 250': 'Krating Daeng 250',
        'red edition': 'Red Edition',
        'sugarfree': 'Sugarfree', 'sugar free': 'Sugarfree',
        'sugarfree ': 'Sugarfree', 'sugar-free': 'Sugarfree',
        'tropical edition': 'Tropical Edition', 'tropical  edition': 'Tropical Edition',
        'tropical': 'Tropical Edition',
    }
    data['Product_Variant'] = data['Product_Variant'].replace(product_variant_mapping)

    data['Channel'] = data['Channel'].str.strip().str.lower()
    channel_mapping = {
        'social media': 'Social Media', 'social_media': 'Social Media',
        'tv ad': 'TV Ad', 'tv ads': 'TV Ad',
        'tv advertisement': 'TV Ad', 'television ad': 'TV Ad',
        'in-store promo': 'In-store Promo',
        'f1 sponsorship': 'F1 Sponsorship',
        'extreme sports': 'Extreme Sports'
    }
    data['Channel'] = data['Channel'].replace(channel_mapping)
    data['Channel'] = data['Channel'].apply(lambda x: x.title() if isinstance(x, str) else x)

    data['Date'] = pd.to_datetime(data['Date'], format='mixed')

    st.success("✅ แก้ไขค่าที่ไม่สอดคล้องกันสำเร็จแล้ว! เย้! 🎉")
    st.write("##### ✨ หลังปรับปรุงค่าที่ไม่สอดคล้องกัน (ค่าที่ไม่ซ้ำกันในคอลัมน์หมวดหมู่)")
    for col in cat_cols:
        unique_vals = data[col].unique()
        st.write(f"**📌 {col} ({len(unique_vals)} ค่า):**")
        st.write(unique_vals)
    return data

def handle_missing_data(data):
    st.subheader("📭 4. จัดการข้อมูลที่หายไป! 🕵️‍♀️")
    missing_count = data.isnull().sum()
    st.write("##### 🔍 จำนวนค่าที่หายไปก่อนแก้ไข:")
    if missing_count.sum() > 0:
        st.dataframe(missing_count[missing_count > 0])

        median_marketing = data['Marketing_Spend'].median()
        data['Marketing_Spend'] = data['Marketing_Spend'].fillna(median_marketing)
        st.info(f'💖 Marketing_Spend: เติมด้วย Median = {median_marketing:,.2f}')

        median_score = data['Customer_Score'].median()
        data['Customer_Score'] = data['Customer_Score'].fillna(median_score)
        st.info(f'🌟 Customer_Score: เติมด้วย Median = {median_score}')

        st.success("✅ แก้ไขข้อมูลที่หายไปสำเร็จแล้ว! Hooray! 🎉")
        st.write("##### ✨ จำนวนค่าที่หายไปหลังแก้ไข:")
        st.write(f"รวม {data.isnull().sum().sum()} ค่า (ควรเป็น 0 นะ! 😇)")
    else:
        st.info("ไม่พบข้อมูลที่หายไปเลย! ข้อมูลของคุณสมบูรณ์แบบ! 💯")
    return data

def handle_noisy_data(data):
    st.subheader("📢 5. จัดการข้อมูลผิดพลาด (Noisy Data)! 🤯")
    st.write("##### 🚨 ตรวจสอบ Business Logic ก่อนแก้ไข:")
    neg_price = data[data['Unit_Price'] <= 0]
    neg_units = data[data['Units_Sold'] <= 0]
    neg_mkt = data[data['Marketing_Spend'] < 0]
    bad_score = data[(data['Customer_Score'] < 1) | (data['Customer_Score'] > 10)]

    found_noisy = False
    if len(neg_price) > 0:
        st.warning(f"❌ Unit_Price ≤ 0 : พบ {len(neg_price):,} แถว (ราคาต้องเป็นบวกเท่านั้นนะ! 💰)")
        found_noisy = True
    if len(neg_units) > 0:
        st.warning(f"❌ Units_Sold ≤ 0 : พบ {len(neg_units):,} แถว (ขายไม่ได้ติดลบนะ! 🛍️)")
        found_noisy = True
    if len(neg_mkt) > 0:
        st.warning(f"❌ Marketing < 0 : พบ {len(neg_mkt):,} แถว (งบต้องไม่ติดลบนะ! 📉)")
        found_noisy = True
    if len(bad_score) > 0:
        st.warning(f"❌ Customer_Score ไม่ใช่ 1-10: พบ {len(bad_score):,} แถว (คะแนนต้องอยู่ระหว่าง 1-10 เท่านั้น! ⭐)")
        found_noisy = True

    if found_noisy:
        initial_rows = len(data)
        data = data[data['Unit_Price'] > 0]
        data = data[data['Units_Sold'] > 0]
        data = data[data['Marketing_Spend'] >= 0]
        data = data[(data['Customer_Score'] >= 1) & (data['Customer_Score'] <= 10)]
        st.success(f"✅ แก้ไข Noisy Data สำเร็จแล้ว! ลบไป {initial_rows - len(data):,} แถว 🗑️")
    else:
        st.info("ไม่พบ Noisy Data ที่ขัดแย้งกับ Business Logic เลย! ข้อมูลของคุณสะอาดมาก! 🫧")
    return data

def perform_outlier_analysis(data):
    st.subheader("📐 6. ตรวจจับและดูแล Outliers! 🔭")
    st.markdown("##### 🔍 ตรวจสอบ Outliers ด้วย Boxplot:")

    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if 'Customer_Score' in numeric_cols:
        numeric_cols.remove('Customer_Score')

    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots(figsize=(8, 2))
            sns.boxplot(x=data[col], ax=ax)
            ax.set_title(f'Boxplot ของ {col}')
            st.pyplot(fig)
            plt.close(fig)

        st.markdown("""
        **✨ หมายเหตุพิเศษเกี่ยวกับการจัดการ Outliers: ✨**
        ใน Workshop แสนสนุกนี้ เราอาจพบว่าการใช้ `winsorize` เพื่อปรับค่า Outliers ในบางคอลัมน์ (เช่น `Units_Sold`) อาจทำให้ Business Logic ของข้อมูลเปลี่ยนไปได้นะ 🧐 (เช่น ยอดขายที่ถูกปรับอาจไม่สะท้อนยอดขายจริง)
        ดังนั้น เพื่อรักษาความถูกต้องของข้อมูลตามบริบททางธุรกิจ เราจะเลือก **ไม่ปรับ Outliers** ในขั้นตอนนี้จ้า! 💖 แต่ในสถานการณ์จริง การตัดสินใจเรื่อง Outliers ต้องพิจารณาอย่างรอบคอบจากบริบทและเป้าหมายการวิเคราะห์เป็นหลักนะ! 💡
        """)
    else:
        st.info("ไม่พบคอลัมน์ตัวเลขที่เหมาะสำหรับการวิเคราะห์ Outliers เลย! 🔢")
    return data

def clean_data_pipeline(df_input, do_explore, do_duplicates, do_inconsistent, do_missing, do_noisy, do_outlier):
    df_cleaned = df_input.copy()
    if do_explore:
        df_cleaned = perform_data_exploration(df_cleaned)
    if do_duplicates:
        df_cleaned = handle_duplicate_data(df_cleaned)
    if do_inconsistent:
        df_cleaned = handle_inconsistent_data(df_cleaned)
    if do_missing:
        df_cleaned = handle_missing_data(df_cleaned)
    if do_noisy:
        df_cleaned = handle_noisy_data(df_cleaned)
    if do_outlier:
        df_cleaned = perform_outlier_analysis(df_cleaned)
    return df_cleaned


if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    df = df_raw.copy()
    st.success("ไฟล์อัปโหลดสำเร็จแล้ว! พร้อมลุย! 🚀")
    st.write("### ข้อมูลดิบสุดน่ารัก (5 แถวแรก) 🧐")
    st.dataframe(df_raw.head())

    st.sidebar.header("🧹 เลือกขั้นตอนการทำความสะอาดข้อมูล 🧼")
    do_explore = st.sidebar.checkbox("1. สำรวจข้อมูลเบื้องต้น ✨", value=True)
    do_duplicates = st.sidebar.checkbox("2. จัดการข้อมูลซ้ำซ้อน 👯", value=True)
    do_inconsistent = st.sidebar.checkbox("3. แก้ไขข้อมูลที่ไม่สอดคล้องกัน 🧩", value=True)
    do_missing = st.sidebar.checkbox("4. จัดการข้อมูลที่หายไป 🕵️‍♀️", value=True)
    do_noisy = st.sidebar.checkbox("5. จัดการข้อมูลผิดพลาด 🤯", value=True)
    do_outlier = st.sidebar.checkbox("6. ตรวจจับและดูแล Outliers 🔭", value=True)

    st.markdown("---  ")

    if st.button("✨ เริ่มต้นการทำความสะอาดข้อมูล! ✨"):
        st.write("### กำลังดำเนินการทำความสะอาดข้อมูล... รอแป๊บนะ! ⏳")
        
        # Call the new cleaning pipeline function
        df = clean_data_pipeline(df_raw, do_explore, do_duplicates, do_inconsistent, do_missing, do_noisy, do_outlier)

        st.markdown("---  ")
        st.subheader("✅ 7. สรุปข้อมูลที่ทำความสะอาดแล้ว! 💖")
        st.write(f"#### ก่อนทำความสะอาด: {df_raw.shape[0]:,} แถว, {df_raw.shape[1]} คอลัมน์")
        st.write(f"#### หลังทำความสะอาด: {df.shape[0]:,} แถว, {df.shape[1]} คอลัมน์")

        st.write("### ข้อมูลที่ทำความสะอาดแล้ว (5 แถวแรก) ✨")
        st.dataframe(df.head())

        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ ดาวน์โหลดข้อมูลที่ทำความสะอาดแล้วเป็น CSV! ⬇️",
            data=csv_buffer,
            file_name="redbull_clean_cute.csv",
            mime="text/csv",
            help="คลิกเพื่อดาวน์โหลดชุดข้อมูลที่สะอาดสดใสของคุณ! 🎉"
        )
else:
    st.info("กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มต้นการผจญภัยทำความสะอาดข้อมูลของคุณ! 📂")

if st.button("🏠 กลับหน้าหลักแอปพลิเคชัน 🏠"):
    st.switch_page("app.py")
