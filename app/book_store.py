"""
Book storage for 1.1 Interactive Digital Books.
Uses JSON for metadata and a folder per book for page images.
"""
import json
import os
import re
import uuid
from pathlib import Path

# Base path for data (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BOOKS_JSON = DATA_DIR / "books.json"
BOOKS_DIR = DATA_DIR / "books"

# Allowed image extensions for pages
PAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

# Default categories (extensible later)
CATEGORIES = ["Fiction", "Non-fiction", "Adventure", "Animal", "Fantasy", "Other"]

# Max pages per book for in-app upload (avoid abuse)
MAX_PAGES_UPLOAD = 100


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    if not BOOKS_JSON.exists():
        BOOKS_JSON.write_text("[]", encoding="utf-8")


def _load_books():
    _ensure_data_dir()
    with open(BOOKS_JSON, encoding="utf-8") as f:
        return json.load(f)


def _save_books(books):
    _ensure_data_dir()
    with open(BOOKS_JSON, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2)


def _slugify(text):
    """Create URL-safe slug from title."""
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-") or "book"


def list_books():
    """Return all books (id, title, category, slug, created_at, page_count)."""
    return _load_books()


def get_book(book_id=None, slug=None):
    """Get one book by id or slug. Returns None if not found."""
    books = _load_books()
    for b in books:
        if book_id and b.get("id") == book_id:
            return b
        if slug and b.get("slug") == slug:
            return b
    return None


def get_book_pages_dir(book_id):
    """Path to folder where page images for this book are stored."""
    return BOOKS_DIR / str(book_id) / "pages"


def get_page_filenames(book_id):
    """Return ordered list of page image filenames (e.g. ['1.png', '2.jpg'])."""
    pages_dir = get_book_pages_dir(book_id)
    if not pages_dir.exists():
        return []
    files = []
    for f in pages_dir.iterdir():
        if f.is_file() and f.suffix.lower() in PAGE_EXTENSIONS:
            files.append(f.name)
    # Sort naturally (1, 2, 10 not 1, 10, 2)
    def sort_key(name):
        base = Path(name).stem
        try:
            return (0, int(base))
        except ValueError:
            return (1, base)

    files.sort(key=sort_key)
    return files


def _ocr_book_pages(book_id):
    """Run OCR on each page image; return list of text strings (same order as get_page_filenames)."""
    from app.ocr import extract_text
    pages_dir = get_book_pages_dir(book_id)
    filenames = get_page_filenames(book_id)
    return [extract_text(pages_dir / fn) for fn in filenames]


def update_book_page_texts(book_id, page_texts):
    """Update stored OCR text for a book. Use for backfilling existing books."""
    books = _load_books()
    for b in books:
        if b.get("id") == book_id:
            b["page_texts"] = list(page_texts)
            _save_books(books)
            return


def create_book(title, category, page_image_paths):
    """
    Create a new book: save metadata and copy page images into data/books/<id>/pages/.
    page_image_paths: list of Path or str to image files (in order).
    Returns the new book dict or None on failure.
    """
    _ensure_data_dir()
    books = _load_books()
    book_id = str(uuid.uuid4())[:8]
    slug = _slugify(title)
    # Ensure slug is unique
    existing_slugs = {b.get("slug") for b in books}
    if slug in existing_slugs:
        slug = f"{slug}-{book_id}"

    pages_dir = get_book_pages_dir(book_id)
    pages_dir.mkdir(parents=True, exist_ok=True)

    page_count = 0
    for i, src in enumerate(page_image_paths, start=1):
        src = Path(src)
        if not src.is_file() or src.suffix.lower() not in PAGE_EXTENSIONS:
            continue
        ext = src.suffix.lower()
        dest = pages_dir / f"{i}{ext}"
        dest.write_bytes(src.read_bytes())
        page_count += 1
    page_texts = _ocr_book_pages(book_id)
    book = {
        "id": book_id,
        "title": title,
        "category": category,
        "slug": slug,
        "page_count": page_count,
        "created_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "page_texts": page_texts,
    }
    books.append(book)
    _save_books(books)
    return book


def create_book_from_uploads(title, category, file_list):
    """
    Create a new book from uploaded file-like objects (e.g. Flask request.files).
    file_list: list of objects with .filename and .save(dest_path) or .read() (in order).
    Saves pages as 1.ext, 2.ext, ... in upload order. Skips non-image files.
    Returns (book_dict, error_message). book_dict is None on failure.
    """
    import datetime
    _ensure_data_dir()
    # Collect valid uploads in order (by extension from filename)
    valid = []
    for f in file_list:
        if not getattr(f, "filename", None) or not f.filename.strip():
            continue
        ext = Path(f.filename).suffix.lower()
        if ext in PAGE_EXTENSIONS:
            valid.append((f, ext))
    if not valid:
        return None, "No valid page images (use .png, .jpg, .jpeg, .webp, .gif)."
    if len(valid) > MAX_PAGES_UPLOAD:
        return None, f"Too many pages (max {MAX_PAGES_UPLOAD})."

    books = _load_books()
    book_id = str(uuid.uuid4())[:8]
    slug = _slugify(title)
    existing_slugs = {b.get("slug") for b in books}
    if slug in existing_slugs:
        slug = f"{slug}-{book_id}"

    pages_dir = get_book_pages_dir(book_id)
    pages_dir.mkdir(parents=True, exist_ok=True)

    page_count = 0
    for i, (f, ext) in enumerate(valid, start=1):
        dest = pages_dir / f"{i}{ext}"
        try:
            if hasattr(f, "save") and callable(f.save):
                f.save(str(dest))
            else:
                dest.write_bytes(f.read())
        except OSError:
            continue
        page_count += 1

    page_texts = _ocr_book_pages(book_id)
    book = {
        "id": book_id,
        "title": title,
        "category": category,
        "slug": slug,
        "page_count": page_count,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "page_texts": page_texts,
    }
    books.append(book)
    _save_books(books)
    return book, None
