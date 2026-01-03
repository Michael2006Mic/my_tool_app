import streamlit as st

# 1. PAGE CONFIG MUST BE FIRST
st.set_page_config(page_title="PDF Summarizer & Visualizer", page_icon="📄")

import requests
import PyPDF2
import fitz  # This is PyMuPDF
import io
import time
from PIL import Image

# --- Header ---
st.title("📄 PDF Summarizer with Images")
st.markdown("Extract text summaries and view images from your documents.")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    if "HF_TOKEN" in st.secrets:
        st.success("token loaded from secrets")
        hf_token = st.secrets["HF_TOKEN"]
    else:
        hf_token = st.text_input("Hugging Face API Token", type="password")
        st.warning("token not found in secrets, please enter it manually")
     
    model_id = st.selectbox(
        "Select Model",
        ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6"]
    )
    chunk_size = st.slider("Chunk Size", 1000, 4000, 2000)

# --- Functions ---

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF text: {e}")
        return None
    return text

def extract_images_from_pdf(pdf_stream):
   
    images = []
    try:
        # Open the PDF from memory stream
        pdf_stream.seek(0)
        doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
               
                image = Image.open(io.BytesIO(image_bytes))
                
                
                if image.width > 100 and image.height > 100:
                    images.append(image)
                    
    except Exception as e:
        st.error(f"Error extracting images: {e}")
        return []
        
    return images

def chunk_text(text, size=2000):
    return [text[i:i+size] for i in range(0, len(text), size)]

def summarize_chunk(token, text_chunk, model):
    api_url = f"https://router.huggingface.co/hf-inference/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": text_chunk,
        "parameters": {"min_length": 30, "max_length": 150, "do_sample": False}
    }
    
    # Retry Loop (5 attempts)
    for attempt in range(5):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text')
                return None
            elif response.status_code in [503, 429]:
                time.sleep((attempt + 1) * 5)
                continue
            else:
                return None
        except:
            time.sleep(2)
            continue
    return None

# --- Main App ---

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    if not hf_token:
        st.warning("Please enter your Hugging Face API Token in the sidebar.")
    else:
        st.write(f"**File:** {uploaded_file.name}")
        
        if st.button("Analyze PDF"):
            
            # 1. Summarization Phase
            with st.spinner("Processing Text..."):
                full_text = extract_text_from_pdf(uploaded_file)

            if full_text:
                chunks = chunk_text(full_text, chunk_size)
                st.info(f"Summarizing {len(chunks)} sections...")
                
                final_summary = []
                progress_bar = st.progress(0)
                
                for i, chunk in enumerate(chunks):
                    summary_text = summarize_chunk(hf_token, chunk, model_id)
                    if summary_text:
                        final_summary.append(summary_text)
                    progress_bar.progress((i + 1) / len(chunks))
                
                # Display Summary
                st.success("Summary Complete!")
                st.subheader("📝 Document Summary")
                st.write(" ".join(final_summary))
                
                st.divider()

                # 2. Image Extraction Phase
                with st.spinner("Extracting Images..."):
                    # We need to reset the file pointer to read it again
                    uploaded_file.seek(0)
                    images = extract_images_from_pdf(uploaded_file)
                
                if images:
                    st.subheader(f"🖼️ Extracted Images ({len(images)})")
                    # Display images in columns
                    cols = st.columns(3) 
                    for i, img in enumerate(images):
                        with cols[i % 3]:
                            st.image(img, use_container_width=True, caption=f"Image {i+1}")
                else:
                    st.info("No substantial images found in this document.")