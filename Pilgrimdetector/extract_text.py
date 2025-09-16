import sys
import os
import PyPDF2
import docx
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np

def preprocess_image(pil_image):
    """Preprocess image for OCR: grayscale, denoise, threshold, deskew."""
    # Convert PIL to OpenCV
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive thresholding (better for uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 31, 2
    )

    # Deskew
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = thresh.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return deskewed

def extract_text_from_pdf(file_path):
    text = ""
    print("DEBUG: Trying to open PDF:", file_path)

    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        print(f"DEBUG: PDF has {total_pages} pages")

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                text += page_text + "\n"
            else:
                print(f"DEBUG: OCR processing page {page_num}...")
                images = convert_from_path(file_path, dpi=300, first_page=page_num, last_page=page_num)
                for img in images:
                    processed = preprocess_image(img)
                    # Tesseract config: improve OCR for multiple lines/columns
                    config = "--psm 6"
                    text += pytesseract.image_to_string(processed, lang="eng", config=config) + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    extracted_text = extract_text(file_path)
    print("------ Extracted Text ------\n")
    print(extracted_text)
