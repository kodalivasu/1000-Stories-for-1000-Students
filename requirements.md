# Requirements — 1.1 Interactive Digital Books

Scope: Storytelling Engine — Interactive digital books (audio, name insertion, alternate endings).  
Audience: Kids; design should be minimal, warm, and visually pleasing.

**v1 scope (in progress):** Upload pages → compile flip book → name + category → open → flip → share link (WhatsApp/email).  
**Next:** Ratings/comments → recommend to person → writer’s voice audio → pronunciation help.

---

## Writer

| ID | Requirement | Notes |
|----|-------------|--------|
| W1 | Upload the pages of the book | Writer can upload numbered page images directly in the app (or via script). Pages stored in order (upload order). Image types: .png, .jpg, .jpeg, .webp, .gif. PDF optional later. |
| W2 | Compile uploaded pages into a flip book | App builds a page-by-page flip experience from uploads. |
| W3 | Name the book | Writer can set a title for the book. |
| W4 | Save the book into a category | e.g. Fiction, Non-fiction; extensible category list. |
| W5 | Delete a book at a later stage | With appropriate confirmation. |
| W6 | Recommend a book to another person in the community | In-app "recommend to…" (select recipient). |
| W7 | Share the link to the book via WhatsApp or email | Generate shareable URL; optional pre-filled message. |
| W8 | Respond to reviewers | Reply to comments/reviews on the book. |

---

## Reader

| ID | Requirement | Notes |
|----|-------------|--------|
| R1 | Search for books by keywords or categories | Keyword search + category filter. |
| R2 | Open the book | From search, library, or shared link. |
| R3 | Flip pages in the book | Next/previous (e.g. swipe or buttons). Header toolbar: book icon + title, undo/redo (prev/next page), page nav (prev, current/total, next), share (dropdown: WhatsApp, email, copy link), print, listen (TTS: read aloud page content in a young Indian girl–style voice; page text from OCR at upload/import, backfill via `scripts/ocr_backfill_books.py`), invite a friend (opens share), close. |
| R4 | Read and review books with ratings and comments | Star rating + free-text comments. |
| R5 | Listen to the book being read in the writer's voice | Audio playback (writer-recorded) per page or whole book. |
| R6 | Get help pronouncing any word in the book | Tap word → hear pronunciation (e.g. TTS or pre-recorded). |

---

## Design

- **Audience:** Kids — less busy, more visually pleasing.
- **References:** Dribbble (children's reading / flipbook), Mobbin (e-reader / library patterns).
- **Principles:** Minimal UI, warm palette, large touch targets, clear hierarchy, restrained playfulness.
- **Reader layout:** Max width 1536px; page area scales up to ~1024px height on large screens. Prev/next flip buttons are overlaid on the page (left/right edges), not on the sides of the container.
- **Book page chrome:** Site top nav (Story Books, Upload your book) stays visible when the reader opens a book. The storybook toolbar (title, undo/redo, page nav, share, print, listen, invite, close) is contained inside a book-viewer card so it clearly applies only to that book.

---

## Future / Out of scope for first version (optional)

- Name insertion (Masterplan).
- Alternate endings / branching (Masterplan).
- Pronunciation: TTS vs pre-recorded per word — TBD.
