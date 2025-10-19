# PyQt Web Browser

A clean, tabbed web browser built with **Python 3.9+**, **PyQt5**, and **Qt WebEngine**. It features a familiar UI (back/forward, reload/stop, home, address bar, new-tab, tab close), Google-powered search from the address bar, and smart URL handling.

---

## ✨ Features
- **Tabbed browsing** with middle‑click to close tabs and a handy **“+”** new‑tab button
- **Navigation controls**: Back, Forward, Reload/Stop, Home
- **Smart address bar**: type a full URL or plain terms to search via Google
- **Per‑tab titles & icons** pulled from the page (where available)
- **Find in page** (Ctrl+F) and **Zoom** (Ctrl+Plus/Minus, Ctrl+0)
- **Persistent window geometry** across sessions

> Built to be minimal, fast, and easy to extend for your own research or demos.

---

## 📦 Project Structure
```
pyqt-web-browser/
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── .editorconfig
├── .gitignore
├── src/
│   └── pyqt_web_browser/
│       ├── __init__.py
│       ├── main.py
│       ├── app.py
│       ├── browser.py
│       ├── utils.py
│       └── ui/
│           └── main_window.py
├── tests/
│   └── test_utils.py
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🚀 Quickstart

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```
> **Note (Linux):** If you encounter missing Qt platform plugins, ensure you have system packages like `libxcb`, `mesa`, and an X server. On headless CI you typically skip GUI tests.

### 3) Run
```bash
python -m pyqt_web_browser
```

---

## 🧪 Tests
Unit tests focus on pure‑Python utilities to keep CI fast and reliable.
```bash
pytest -q
```

---

## 🛠️ Configuration
- **Ruff** + **Black** are configured in `pyproject.toml` for linting/formatting.
- GitHub Actions workflow runs lint + tests on PRs and pushes.

---

## 🧩 Extend It
- Add bookmarks/history using `QWebEngineProfile` & `QWebEngineCookieStore`.
- Add a downloads panel via `QWebEngineView.page().profile().downloadRequested`.
- Wire a custom homepage or per‑tab settings.

---

## 📜 License
MIT — see [LICENSE](LICENSE).

---

## 👤 Author Header Template
All Python files include a professional header with author, dates, and license — matching your GitHub style.

