# 1.1 Interactive Digital Books — v1

Web app: upload pages → flip book → name + category → open → flip → share (WhatsApp/email).

## Run the app

1. **Install:** `pip install -r requirements.txt`
2. **Optional — Listen reads page text:** Install [Tesseract](https://github.com/tesseract-ocr/tesseract) and ensure it’s on your PATH. Then page text is extracted at upload/import; for existing books run `python scripts/ocr_backfill_books.py` once.
3. **Import your first book** (e.g. Diwali & Navratri):  
   From the project root, run:
   ```bash
   python scripts/import_book_from_folder.py "Diwali & Navratri" "Diwali & Navratri" "Fiction"
   ```
   Put your page images in a folder (e.g. **Diwali & Navratri**) in the project root, or use any path. Use the folder path where your page images live (relative to project root or absolute). Allowed: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`. Pages are ordered by filename (1.png, 2.jpg, etc.).
4. **Start server:** `python run.py`
5. **Open:** http://127.0.0.1:5000

## What’s in v1

- **Home:** List books (cover = first page, title, category).
- **Open book:** Click a book → flip view with prev/next and swipe.
- **Share:** WhatsApp and Email buttons with the book link.

## Next (after v1)

- Ratings/comments → Recommend to person → Writer’s voice audio → Pronunciation help.
