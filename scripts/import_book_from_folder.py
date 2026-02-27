"""
Import a book from a folder of page images.
Usage:
  python scripts/import_book_from_folder.py "Diwali & Navratri" "Diwali & Navratri" "Fiction"
  python scripts/import_book_from_folder.py <folder_path> <book_title> <category>

Folder can be relative to project root or absolute.
Images are sorted by filename (1.png, 2.jpg, etc.) and copied into the book's page store.
"""
import sys
from pathlib import Path

# Add project root so we can import app.book_store
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.book_store import (
    PAGE_EXTENSIONS,
    create_book,
    get_book_pages_dir,
    PROJECT_ROOT,
)


def collect_page_paths(folder_path):
    """Return sorted list of image file paths in folder."""
    folder = Path(folder_path)
    if not folder.is_dir():
        return []
    paths = []
    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() in PAGE_EXTENSIONS:
            paths.append(f)
    def sort_key(p):
        stem = p.stem
        try:
            return (0, int(stem))
        except ValueError:
            return (1, stem.lower())
    paths.sort(key=sort_key)
    return paths


def main():
    if len(sys.argv) < 4:
        print("Usage: python import_book_from_folder.py <folder_path> <book_title> <category>")
        print('Example: python scripts/import_book_from_folder.py "Diwali & Navratri" "Diwali & Navratri" "Fiction"')
        sys.exit(1)
    folder_path = sys.argv[1]
    title = sys.argv[2]
    category = sys.argv[3]
    folder = Path(folder_path)
    if not folder.is_absolute():
        folder = PROJECT_ROOT / folder_path
    if not folder.is_dir():
        print(f"Error: folder not found: {folder}")
        sys.exit(1)
    paths = collect_page_paths(folder)
    if not paths:
        print(f"No image files found in {folder} (allowed: .png, .jpg, .jpeg, .webp, .gif)")
        sys.exit(1)
    book = create_book(title, category, paths)
    print(f"Created book: {book['title']} (id={book['id']}, slug={book['slug']}, pages={book['page_count']})")
    print(f"Pages stored in: {get_book_pages_dir(book['id'])}")


if __name__ == "__main__":
    main()
