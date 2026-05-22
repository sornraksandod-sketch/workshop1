import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide", page_title="Super Cute Data Cleaning App")
st.title("✨💖 Super Cute Data Cleaning Web App 💖✨")
st.markdown("--- 🎀 Upload your CSV, clean it with love, and download the sparkling result! 🎀 ---")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# --- Data Cleaning Functions ---
def handle_duplicates(df):
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates()
    removed_rows = initial_rows - len(df_cleaned)
    if removed_rows > 0:
        st.success(f"✅ Removed {removed_rows:,} duplicate rows. Phew! 😮‍💨")
    else:
        st.info("No duplicate rows found. Your data is already super neat! ✨")
    return df_cleaned

def handle_missing_values(df):
    missing_before = df.isnull().sum().sum()
    if missing_before == 0:
        st.info("No missing values found. Perfect! 💯")
        return df

    st.subheader("Filling in the blanks... 🕵️‍♀️")
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype in ['int64', 'float64']:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                st.info(f"💖 Filled missing values in '{col}' with median: {median_val:,.2f}")
            elif df[col].dtype == 'object':
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                st.info(f"🌟 Filled missing values in '{col}' with mode: '{mode_val}'")
            else:
                df[col] = df[col].fillna(df[col].mode()[0]) # Fallback for other types
                st.info(f"🌈 Filled missing values in '{col}' with mode.")
    missing_after = df.isnull().sum().sum()
    if missing_after == 0:
        st.success("All missing values handled! Hooray! 🎉")
    return df

# --- Main App Logic ---
if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    df = df_raw.copy()
    st.success("File uploaded successfully! Let's get cleaning! 🚀")
    st.write("### Original Data (First 5 Rows) 🧐")
    st.dataframe(df_raw.head())

    st.sidebar.header("🧹 Cleaning Choices 🧹")
    clean_duplicates = st.sidebar.checkbox("Remove Duplicate Rows (Deduplicate!)", value=True)
    clean_missing = st.sidebar.checkbox("Handle Missing Values (Fill in the blanks!)", value=True)

    st.markdown("---  ")

    if st.button("✨ Start My Cleaning Adventure! ✨"):
        st.write("### Your Cleaning Adventure is Underway! ⏳")

        if clean_duplicates:
            df = handle_duplicates(df)
        
        if clean_missing:
            df = handle_missing_values(df)
        
        st.markdown("---  ")
        st.subheader("💖 Cleaning Complete! Here's Your Sparkling Data! 💖")
        st.write(f"#### Original Rows: {df_raw.shape[0]:,}")
        st.write(f"#### Cleaned Rows: {df.shape[0]:,}")

        st.write("### Cleaned Data (First 5 Rows) ✨")
        st.dataframe(df.head())

        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download My Cleaned Data! ⬇️",
            data=csv_buffer,
            file_name="super_cute_cleaned_data.csv",
            mime="text/csv",
            help="Click to download your beautifully cleaned dataset! 🎉"
        )
else:
    st.info("Please upload a CSV file to start your data cleaning journey! 📂")

if st.button("🏠 กลับหน้าหลัก"):
    st.switch_page("app.py")
