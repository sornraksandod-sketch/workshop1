import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide", page_title="Simple Data Cleaning App")
st.title("✨ Simple Data Cleaning Web App")
st.markdown("--- Upload your CSV, clean it, and download the result! ---")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# --- Data Cleaning Functions ---
def handle_duplicates(df):
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates()
    removed_rows = initial_rows - len(df_cleaned)
    if removed_rows > 0:
        st.success(f"✅ Removed {removed_rows:,} duplicate rows.")
    else:
        st.info("No duplicate rows found.")
    return df_cleaned

def handle_missing_values(df):
    missing_before = df.isnull().sum().sum()
    if missing_before == 0:
        st.info("No missing values found.")
        return df

    st.subheader("Handling Missing Values")
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype in ['int64', 'float64']:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                st.info(f"✅ Filled missing values in '{col}' with median: {median_val:,.2f}")
            elif df[col].dtype == 'object':
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                st.info(f"✅ Filled missing values in '{col}' with mode: '{mode_val}'")
            else:
                df[col] = df[col].fillna(df[col].mode()[0]) # Fallback for other types
                st.info(f"✅ Filled missing values in '{col}' with mode.")
    missing_after = df.isnull().sum().sum()
    if missing_after == 0:
        st.success("All missing values handled.")
    return df

# --- Main App Logic ---
if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    df = df_raw.copy()
    st.success("File uploaded successfully!")
    st.write("### Raw Data (First 5 Rows)")
    st.dataframe(df_raw.head())

    st.sidebar.header("Cleaning Options")
    clean_duplicates = st.sidebar.checkbox("Remove Duplicate Rows", value=True)
    clean_missing = st.sidebar.checkbox("Handle Missing Values (Median/Mode Imputation)", value=True)

    st.markdown("---  ")

    if st.button("Perform Cleaning"):
        st.write("### Cleaning in Progress...")

        if clean_duplicates:
            df = handle_duplicates(df)
        
        if clean_missing:
            df = handle_missing_values(df)
        
        st.markdown("---  ")
        st.subheader("✅ Cleaning Summary")
        st.write(f"#### Original Rows: {df_raw.shape[0]:,}")
        st.write(f"#### Cleaned Rows: {df.shape[0]:,}")

        st.write("### Cleaned Data (First 5 Rows)")
        st.dataframe(df.head())

        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=csv_buffer,
            file_name="simple_cleaned_data.csv",
            mime="text/csv",
            help="Click to download the cleaned dataset."
        )
else:
    st.info("Please upload a CSV file to start cleaning.")
