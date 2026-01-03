import streamlit as st
import os
from pdf2docx import Converter

st.set_page_config(page_title="PDF to Word", page_icon="🔄")

st.title("🔄 PDF to Word Converter")
st.markdown("Convert PDF files to editable Word documents. (Linux/Cloud Compatible)")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

if uploaded_pdf:
    if st.button("Convert to DOCX"):
        with st.spinner("Converting..."):
            # 1. Save uploaded file temporarily
            with open("temp_input.pdf", "wb") as f:
                f.write(uploaded_pdf.getbuffer())

            output_filename = "converted.docx"
            
            try:
                # 2. Convert
                cv = Converter("temp_input.pdf")
                cv.convert(output_filename, start=0, end=None)
                cv.close()
                
                # 3. Download Button
                with open(output_filename, "rb") as f:
                    st.download_button(
                        label="Download Word Doc",
                        data=f,
                        file_name="converted.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("Conversion Successful!")
                
            except Exception as e:
                st.error(f"Error during conversion: {e}")
            
            finally:
                # Cleanup
                if os.path.exists("temp_input.pdf"): os.remove("temp_input.pdf")
                if os.path.exists(output_filename): os.remove(output_filename)