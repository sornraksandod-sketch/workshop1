import streamlit as st

st.set_page_config(page_title="MyApp", layout="wide")

st.title("🏠 หน้าหลัก ")
st.write("### Boot Camp: Data Science and Machine Learning")
st.info("7 Day Intensive Hands-on Workshop")
st.write("Sornrak")
st.write("##### Day 1: การจัดการข้อมูลพื้นฐานและโครงสร้างข้อมูลด้วย Python")

if st.button("full_clean_kie"):
    st.switch_page("pages/cute_full_clean_kie.py")
elif st.button("การแปลงข้อมูล"):
    st.switch_page("pages/app1_discount_calc.py")
elif st.button("การวิเคราะห์ข้อมูลเชิงสำรวจ"):
    st.switch_page("pages/app1_discount_calc.py")    
elif st.button("การพยากรณ์ยอดขายแบบง่าย"):
    st.switch_page("pages/app1_discount_calc.py")   
elif st.button("การพยากรณ์ระยะเวบาการให้บริการขนส่ง"):
    st.switch_page("pages/app1_discount_calc.py")   
