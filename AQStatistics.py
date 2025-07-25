import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

st.set_page_config(page_title="Clean Air Blue Paper Dashboard", layout="wide")

st.title("📘 Clean Air Blue Paper Dashboard")
st.markdown("Explore key statistics from Thailand's Clean Air Blue Paper.")

# File uploader
uploaded_file = st.file_uploader("Upload the Clean_Air_Blue_Paper_EN.pdf", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    st.sidebar.header("PDF Page Extractor")
    start_page = st.sidebar.number_input("Start Page", min_value=1, max_value=len(doc), value=20)
    end_page = st.sidebar.number_input("End Page", min_value=start_page, max_value=len(doc), value=21)

    def extract_text(start, end):
        text = ""
        for i in range(start-1, end):
            text += doc[i].get_text()
        return text

    extracted_text = extract_text(start_page, end_page)
    st.subheader("📝 Extracted Text")
    st.text_area("Raw text from selected pages:", extracted_text, height=300)

    # Vehicle data extraction from known structure (page 20–21 in original)
    if st.button("Generate Sample Visualization: Registered Cars"):
        matches = re.findall(r'(\d{4})\s+([0-9.,]+)\s+([0-9.,]+)', extracted_text)
        data = []
        for year, bkk, other in matches:
            try:
                data.append({
                    "Year": int(year),
                    "Bangkok": float(bkk.replace(",", "")),
                    "Other Provinces": float(other.replace(",", ""))
                })
            except:
                continue
        if data:
            df = pd.DataFrame(data)
            df.set_index("Year", inplace=True)

            st.subheader("📊 Registered Cars Over Time")
            st.line_chart(df)

            st.download_button(
                label="📥 Download Data as CSV",
                data=df.to_csv().encode(),
                file_name="registered_cars.csv",
                mime="text/csv"
            )
        else:
            st.warning("No structured vehicle data found in selected text.")
