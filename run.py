"""
Run the 1.1 Interactive Digital Books web app.
  python run.py
Then open http://127.0.0.1:5000
"""
import os
import sys

# Project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.web import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
