# Technical Design — 1,000 Stories for 1,000 Students

Technical architecture and design for the Interactive Digital Books application. Product context: **Masterplan.md**, **PRD.md**, **requirements.md**.

---

## 1. Overview

### 1.1 Purpose

- **Writers** upload or import page images to create storybooks (title, category).
- **Readers** browse books, open a flip-book view, flip pages, share links, print, and use **Listen** (TTS with OCR-derived page text in a young Indian girl–style voice).

### 1.2 Tech Stack

| Layer        | Choice              | Notes                                      |
|-------------|---------------------|--------------------------------------------|
| Backend     | Python 3, Flask     | Routes, book storage, template rendering   |
| Data        | JSON + filesystem   | `data/books.json`, `data/books/<id>/pages/`|
| OCR         | Tesseract + pytesseract, Pillow | Optional; fallback to no page text if unavailable |
| Frontend    | HTML, CSS, vanilla JS | No framework; server-rendered + minimal JS |
| TTS         | Browser Web Speech API (SpeechSynthesis) | Voice selection + pitch for Listen       |

### 1.3 Out of Scope (Current)

- Auth, user accounts, ratings/comments, writer-recorded audio, pronunciation help, name insertion, alternate endings. See Masterplan and PRD for roadmap.

---

## 2. Architecture

### 2.1 High-Level Flow

```
[Writer]  Upload/import → Flask API → book_store → JSON + page images + OCR → books.json + data/books/<id>/pages/
[Reader]  Open book → Flask book_view → book.html + page_texts → Listen (TTS) reads title + page text from OCR
```

### 2.2 Directory Layout

```
project/
├── app/
│   ├── web.py          # Flask app, routes (/, /book/<slug>, /upload, /api/books, /book/<id>/pages/<path>)
│   ├── book_store.py   # Book CRUD, page filenames, OCR orchestration, page_texts
│   └── ocr.py          # OCR: extract_text(image_path) via Tesseract/Pillow
├── data/
│   ├── books.json      # List of { id, title, category, slug, page_count, created_at, page_texts? }
│   └── books/
│       └── <book_id>/
│           └── pages/  # 1.png, 2.jpg, ... (ordered by numeric stem)
├── static/
│   ├── style.css
│   └── book.js         # Flip, share, Listen (TTS + voice selection), print
├── templates/
│   ├── index.html      # Home: list books
│   ├── book.html       # Reader: flip view, toolbar, page image, script vars (pages, pageTexts, etc.)
│   └── upload.html     # Writer: upload form
├── scripts/
│   ├── import_book_from_folder.py  # Create book from folder of images (calls create_book + OCR)
│   └── ocr_backfill_books.py      # Backfill page_texts for existing books
├── requirements.txt   # Flask, Pillow, pytesseract
└── run.py             # Entry point: run Flask dev server
```

### 2.3 Data Model

**Book (in `books.json`):**

| Field         | Type     | Description |
|---------------|----------|-------------|
| id            | string   | Short unique id (e.g. 8-char) |
| title         | string   | Display title |
| category      | string   | One of CATEGORIES |
| slug          | string   | URL-safe, unique (e.g. book view URL) |
| page_count    | int      | Number of page images |
| created_at    | string   | ISO 8601 UTC |
| page_texts    | [string] | Optional; OCR text per page, same order as pages |

**Pages:** Stored as files under `data/books/<book_id>/pages/`. Ordered by numeric filename stem (1, 2, …). No separate page metadata table.

---

## 3. Key Components

### 3.1 Book Storage (`app/book_store.py`)

- **list_books()** — Load all books from `books.json`.
- **get_book(book_id=None, slug=None)** — Return one book or None.
- **get_book_pages_dir(book_id)** — Path to `data/books/<id>/pages/`.
- **get_page_filenames(book_id)** — Sorted list of page image filenames (natural sort by number).
- **create_book(title, category, page_image_paths)** — Allocate id/slug, copy images, run OCR, save `page_texts`, append to `books.json`. Used by import script.
- **create_book_from_uploads(title, category, file_list)** — Same for web upload; returns (book, error_message).
- **_ocr_book_pages(book_id)** — Run OCR on each page (via `app.ocr.extract_text`); return list of strings.
- **update_book_page_texts(book_id, page_texts)** — Backfill: update one book's `page_texts` in `books.json`.

### 3.2 OCR (`app/ocr.py`)

- **extract_text(image_path)** — Opens image with Pillow, runs `pytesseract.image_to_string(img)`, returns stripped text or `""` on any failure (Tesseract missing, bad image, etc.). No exceptions propagated; allows app to run without Tesseract (Listen falls back to title + page number only).
- **Tesseract path:** By default pytesseract uses `tesseract` from PATH. If Python's environment doesn't see PATH (e.g. some IDEs), set `pytesseract.pytesseract.tesseract_cmd` to the full path to `tesseract.exe` (or configure per-deployment).

### 3.3 Web Routes (`app/web.py`)

- **GET /** — Home; list books; add `cover` (first page filename) per book.
- **GET /book/<slug>** — Book view; load book and page filenames; derive `page_texts` (align length with pages, pad/trim); render `book.html` with book, pages, page_texts.
- **GET /upload** — Upload form (categories from CATEGORIES).
- **POST /api/books** — Create book from form (title, category, pages); return JSON { ok, book, slug } or error.
- **GET /book/<book_id>/pages/<path:filename>** — Serve single page image from book's pages dir.

### 3.4 Reader Frontend (`static/book.js`)

- **State:** currentPage, page image src, indicators.
- **Navigation:** prev/next (buttons + optional swipe); undo/redo mapped to prev/next; header page nav.
- **Share:** Dropdown (WhatsApp, email, copy link); share link built from base URL + book slug.
- **Listen:** Dropdown (Read aloud, Stop). On Read aloud: build string = title + "Page N. " + (pageTexts[currentPage] if present) or "Page N of M."; SpeechSynthesisUtterance with rate 0.9, pitch 1.2; voice selection prefers en-IN female then any en-IN then English female; speak. Stop cancels synthesis.
- **Print:** window.print(). Invite opens share dropdown.

### 3.5 Listen (TTS) Design

- **Input:** bookTitle, currentPage, pages.length, pageTexts[] (from template).
- **Voice:** Young Indian girl–style: prefer Indian English female, else any en-IN, else English female; pitch 1.2 for younger sound.
- **Content:** If pageTexts[currentPage] has text, speak "<Title>. Page <n>. <page text>"; else "<Title>. Page <n> of <total>."
- **Dependencies:** Browser Web Speech API; no server-side TTS.

---

## 4. Cross-Cutting Concerns

### 4.1 Security / Robustness

- Upload: max page count (MAX_PAGES_UPLOAD), allowed image extensions; no auth in current scope.
- Page image serving: book must exist; filename served from that book's pages dir only (no path traversal beyond that).
- OCR: failures contained; no user-controlled input to Tesseract except image path (project-controlled).

### 4.2 Deployment

- Dev: `python run.py` (Flask dev server).
- Prod: Use a production WSGI server (e.g. Gunicorn) behind a reverse proxy; static files served by app or proxy.
- Tesseract: Optional; install and ensure executable is on PATH or set `tesseract_cmd` in OCR so backfill and upload/import OCR work in the same environment.

### 4.3 Scripts

- **import_book_from_folder.py** — Args: folder_path, title, category. Collects images (by PAGE_EXTENSIONS), sorts by numeric stem, calls create_book(); creates book with page_texts.
- **ocr_backfill_books.py** — For each book in list_books(), runs _ocr_book_pages(book_id), update_book_page_texts(book_id, page_texts). Use when Tesseract was not available at create time or to re-run OCR.

---

## 5. Future Considerations (Not Implemented)

- **Auth:** Session in signed cookie; require_session(api=True|False) for protected routes (per AGENTS.md).
- **Writer's voice / pronunciation:** R5, R6 in requirements; may add stored audio or word-level TTS.
- **Ratings, comments, recommendations:** v1.1, v1.2; will need additional data models and routes.
- **Name insertion, alternate endings:** Masterplan; may affect content model and reader UI.

---

## 6. References

- **Masterplan.md** — Vision, reading lab, name insertion, alternate endings.
- **PRD.md** — 1.1 product framing, v1–v1.4.
- **requirements.md** — Writer/Reader/Design requirements (W1–W8, R1–R6).
- **AGENTS.md** — How we build, plan-before-coding, doc updates (requirements, PRD).
