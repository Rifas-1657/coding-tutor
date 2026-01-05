"""
Build RAG Index from Lab Manuals
Extracts text and images from PDFs, creates FAISS indexes.
"""

import os
import faiss
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from sentence_transformers import SentenceTransformer

# Configuration
PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Lab")
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "indexes")
META_DIR = os.path.join(os.path.dirname(__file__), "metadata")

# Create directories
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# Tesseract path (Windows)
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk(text, size=180, overlap=40):
    """Split text into chunks with overlap."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + size]))
        i += size - overlap
    return chunks


def build_index(pdf_file: str):
    """Build FAISS index for a single PDF."""
    if not pdf_file.endswith(".pdf"):
        return
    
    subject = pdf_file.replace(".pdf", "")
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    
    if not os.path.exists(pdf_path):
        print(f"Warning: {pdf_path} not found")
        return
    
    print(f"\n📘 Processing {subject}")
    
    doc = fitz.open(pdf_path)
    all_chunks = []
    
    img_subdir = os.path.join(IMG_DIR, subject)
    os.makedirs(img_subdir, exist_ok=True)
    
    # Extract text
    for page in doc:
        text = page.get_text()
        if text.strip():
            all_chunks.extend(chunk(text))
    
    # Extract images and OCR
    img_id = 0
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base = doc.extract_image(xref)
            
            img_path = os.path.join(img_subdir, f"{img_id}.png")
            with open(img_path, "wb") as f:
                f.write(base["image"])
            
            try:
                ocr_text = pytesseract.image_to_string(Image.open(img_path))
                if ocr_text.strip():
                    all_chunks.extend(chunk(ocr_text))
            except Exception as e:
                print(f"Warning: OCR failed for image {img_id}: {e}")
            
            img_id += 1
    
    if not all_chunks:
        print(f"Warning: No content extracted from {subject}")
        return
    
    # Create FAISS index
    embeddings = model.encode(all_chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    
    # Save index and metadata
    faiss.write_index(index, os.path.join(INDEX_DIR, f"{subject}.index"))
    np.save(os.path.join(META_DIR, f"{subject}.npy"), np.array(all_chunks, dtype=object))
    
    print(f"✅ Indexed {subject} | Chunks: {len(all_chunks)}")


def main():
    """Build indexes for all PDFs in Lab directory."""
    if not os.path.exists(PDF_DIR):
        print(f"Error: Lab directory not found: {PDF_DIR}")
        return
    
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    
    for pdf_file in pdf_files:
        build_index(pdf_file)
    
    print("\n✅ Index building complete!")


if __name__ == "__main__":
    main()

