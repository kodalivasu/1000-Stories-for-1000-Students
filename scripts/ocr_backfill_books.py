"""
Backfill OCR text for existing books (so Listen can read page content).
Run once after adding OCR: python scripts/ocr_backfill_books.py

Requires Tesseract installed (see README or requirements).
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.book_store import _ocr_book_pages, list_books, update_book_page_texts


def main():
    books = list_books()
    if not books:
        print("No books found.")
        return
    for book in books:
        bid = book["id"]
        title = book.get("title", "?")
        print(f"OCR: {title} (id={bid}) ...")
        page_texts = _ocr_book_pages(bid)
        update_book_page_texts(bid, page_texts)
        total = sum(len(t) for t in page_texts)
        print(f"  -> {len(page_texts)} pages, {total} chars extracted.")
    print("Done.")


if __name__ == "__main__":
    main()
