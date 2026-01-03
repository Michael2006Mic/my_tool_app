import streamlit as st
import os
import subprocess
from pdf2docx import Converter

st.set_page_config(page_title="Document Converter", page_icon="🔄")

st.title("🔄 Document Converter")
st.markdown("Convert files securely on the cloud.")

# Create Tabs
tab1, tab2 = st.tabs(["📄 PDF to Word", "📝 Word to PDF"])

# ==========================================
# TAB 1: PDF TO WORD
# ==========================================
with tab1:
    st.header("PDF to Word")
    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf", key="pdf")

    if uploaded_pdf and st.button("Convert to DOCX"):
        with st.spinner("Converting..."):
            with open("temp_input.pdf", "wb") as f:
                f.write(uploaded_pdf.getbuffer())

            try:
                cv = Converter("temp_input.pdf")
                cv.convert("converted.docx", start=0, end=None)
                cv.close()
                
                with open("converted.docx", "rb") as f:
                    st.download_button("Download DOCX", f, "converted.docx")
                st.success("Success!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                # Cleanup
                if os.path.exists("temp_input.pdf"): os.remove("temp_input.pdf")
                if os.path.exists("converted.docx"): os.remove("converted.docx")

# ==========================================
# TAB 2: WORD TO PDF (LibreOffice)
# ==========================================
with tab2:
    st.header("Word to PDF")
    uploaded_docx = st.file_uploader("Upload Word Doc", type=["docx", "doc"], key="word")

    if uploaded_docx and st.button("Convert to PDF"):
        with st.spinner("Converting... (This uses LibreOffice)"):
            
            # 1. Save uploaded file
            input_path = "temp_input.docx"
            output_folder = "."  # Current directory
            output_file = "temp_input.pdf" # LibreOffice keeps original name but changes extension
            
            with open(input_path, "wb") as f:
                f.write(uploaded_docx.getbuffer())

            try:
                # 2. Run LibreOffice Command (Linux/Cloud compatible)
                # This command runs LibreOffice in "headless" mode (no GUI) to convert files
                cmd = [
                    'libreoffice', '--headless', '--convert-to', 'pdf', 
                    '--outdir', output_folder, 
                    input_path
                ]
                
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Check if the PDF was created
                if os.path.exists(output_file):
                    st.success("Conversion Successful!")
                    with open(output_file, "rb") as f:
                        st.download_button("Download PDF", f, "converted.pdf")
                else:
                    st.error("Conversion failed. LibreOffice might not be installed on this server.")
                    # Print errors for debugging if needed
                    # st.code(process.stderr.decode())

            except Exception as e:
                st.error(f"System Error: {e}")
            
            finally:
                # Cleanup
                if os.path.exists(input_path): os.remove(input_path)
                if os.path.exists(output_file): os.remove(output_file)
