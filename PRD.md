# Product Requirements — 1,000 Stories for 1,000 Students

High-level product framing. Detailed feature requirements live in **requirements.md** (e.g. 1.1 Interactive Digital Books).

---

## 1.1 Interactive Digital Books

**Vision (Masterplan):** Interactive digital books with audio, name insertion, alternate endings.

**v1 (current):**
- Writer: Upload numbered pages in the app or ingest from a folder (script) → app compiles flip book; book has name + category. Share link via WhatsApp/email.
- Reader: Home lists books; open book → flip pages (buttons + swipe). Site top nav (Story Books, Upload your book) remains on the book page; storybook toolbar (title, book icon, undo/redo, page nav, share, print, listen, invite, close) is inside a book-viewer card so it applies only to that book. Listen uses TTS in a young Indian girl–style voice (en-IN when available, higher pitch for 8-year-old feel). Share link via toolbar or below.
- Implementation: Flask web app, mobile-responsive; data in `data/books.json` + `data/books/<id>/pages/`. OCR (Tesseract) extracts page text at upload/import for Listen; existing books: `scripts/ocr_backfill_books.py`. Writer upload via `/upload` + `POST /api/books`; import via `scripts/import_book_from_folder.py`. Reader: 1536px max width, larger page area on big screens; flip buttons on the page (overlay) not on the sides.

**v1.1 (next):** Ratings and comments on books.

**v1.2:** Recommend book to another person in the community.

**v1.3:** Writer’s voice audio (listen to book read aloud).

**v1.4:** Pronunciation help (tap word → hear pronunciation).

**Later:** Name insertion, alternate endings (Masterplan).

---

*When adding or changing features, update requirements.md and this PRD and note the change.*
