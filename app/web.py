"""
Flask web app for 1.1 Interactive Digital Books (v1).
Routes: home (list books), book (flip view), serve page images, share URL.
"""
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory, url_for

from app.book_store import (
    BOOKS_DIR,
    CATEGORIES,
    create_book_from_uploads,
    get_book,
    get_book_pages_dir,
    get_page_filenames,
    list_books,
)

app = Flask(__name__, static_folder="../static", template_folder="../templates")


@app.route("/")
def index():
    """Home: list all books (title, category, cover = first page)."""
    books = list_books()
    for b in books:
        pages = get_page_filenames(b["id"])
        b["cover"] = pages[0] if pages else None
    return render_template("index.html", books=books)


@app.route("/book/<slug>")
def book_view(slug):
    """Open book by slug; flip book view."""
    book = get_book(slug=slug)
    if not book:
        abort(404)
    pages = get_page_filenames(book["id"])
    page_texts = book.get("page_texts") or []
    # Align length with pages (pad with empty strings if needed)
    while len(page_texts) < len(pages):
        page_texts.append("")
    page_texts = page_texts[: len(pages)]
    return render_template("book.html", book=book, pages=pages, page_texts=page_texts)


@app.route("/upload", methods=["GET"])
def upload_page():
    """Writer: upload page form (title, category, multiple page images)."""
    return render_template("upload.html", categories=CATEGORIES)


@app.route("/api/books", methods=["POST"])
def api_create_book():
    """Create a book from uploaded page images. Form: title, category, pages (multiple files)."""
    title = (request.form.get("title") or "").strip()
    category = (request.form.get("category") or "").strip()
    if not title:
        return jsonify({"ok": False, "error": "Title is required."}), 400
    if not category:
        return jsonify({"ok": False, "error": "Category is required."}), 400
    if category not in CATEGORIES:
        return jsonify({"ok": False, "error": f"Category must be one of: {', '.join(CATEGORIES)}."}), 400
    files = request.files.getlist("pages")
    if not files:
        return jsonify({"ok": False, "error": "At least one page image is required."}), 400
    book, err = create_book_from_uploads(title, category, files)
    if err:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "book": book, "slug": book["slug"]}), 201


@app.route("/book/<book_id>/pages/<path:filename>")
def book_page_image(book_id, filename):
    """Serve a single page image for a book."""
    book = get_book(book_id=book_id)
    if not book:
        abort(404)
    pages_dir = get_book_pages_dir(book_id)
    if not pages_dir.exists():
        abort(404)
    return send_from_directory(pages_dir, filename)


@app.context_processor
def inject_share():
    """Make base_url available in templates for share links."""
    from flask import request
    def base_url():
        return request.url_root.rstrip("/")
    return dict(base_url=base_url)
