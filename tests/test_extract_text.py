import os
from pilgrimdetector.extract_text import extract_text

def test_txt_extraction(tmp_path):
    # create a temp text file
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello World from TXT")

    text = extract_text(str(file_path))
    assert "Hello World from TXT" in text

def test_docx_extraction(tmp_path):
    import docx
    file_path = tmp_path / "sample.docx"
    doc = docx.Document()
    doc.add_paragraph("Hello from DOCX")
    doc.save(file_path)

    text = extract_text(str(file_path))
    assert "Hello from DOCX" in text

def test_pdf_extraction(tmp_path):
    from reportlab.pdfgen import canvas
    file_path = tmp_path / "sample.pdf"

    # create a simple PDF with ReportLab
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello from PDF")
    c.save()

    text = extract_text(str(file_path))
    assert "Hello from PDF" in text
