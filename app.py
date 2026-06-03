import streamlit as st

st.set_page_config(page_title="MyApp", layout="wide")

st.title("🏠 หน้าหลัก ")
st.write("### Boot Camp: Data Science and Machine Learning")
st.info("7 Day Intensive Hands-on Workshop")
st.write("Sornrak")
st.write("##### Day 1: การจัดการข้อมูลพื้นฐานและโครงสร้างข้อมูลด้วย Python")
st.markdown(''':rainbow[Sornrak] ''')

if st.button("Full_clean"):
    st.switch_page("pages/cute_full_clean_kie.py")
elif st.button("Simple_clean_cute"):
    st.switch_page("pages/simple_clean_cute_kie.py")
elif st.button("Simple_clean"):
    st.switch_page("pages/simple_clean_kie.py")    
elif st.button("Transform"):
    st.switch_page("pages/transform_app.py")  
elif st.button("EDA APP"):
    st.switch_page("pages/EDA_app.py")  
