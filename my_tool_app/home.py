import streamlit as st

st.set_page_config(
    page_title="AI Document Suite",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AI Document Suite")
st.markdown("""
### Welcome to your All-in-One Document Tool
This application provides free, open-source tools to handle your documents securely.

**👈 Select a tool from the sidebar to get started.**

#### 🛠️ Available Tools:
1.  **📄 AI Summarizer:** Summarize long PDFs and extract images using advanced AI.
2.  **🔄 PDF Converter:** Convert PDF files to editable Word documents instantly.
3.  **🖼️ Image OCR:** Extract text from scanned images or photos.

---
*Built with Streamlit & Hugging Face.*
""")

st.sidebar.markdown("[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-yellow.svg)](https://www.buymeacoffee.com/Michael2025)")
with st.sidebar:

    st.info("🎈 Like this tool? Share it with a friend!")
