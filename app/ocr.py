"""
Extract text from page images (OCR) for the Listen feature.
Uses Tesseract via pytesseract. If Tesseract is not installed, returns empty string.
"""
from pathlib import Path


def extract_text(image_path):
    """
    Run OCR on an image file. Returns extracted text or empty string on failure.
    image_path: Path or str to a single image (png, jpg, etc.).
    """
    path = Path(image_path)
    if not path.is_file():
        return ""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(path)
        text = pytesseract.image_to_string(img).strip()
        return text if text else ""
    except Exception:
        return ""
