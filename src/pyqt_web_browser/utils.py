#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Utility helpers for the browser, including URL normalization and search query handling.

Usage:
from pyqt_web_browser.utils import url_from_user_input

Notes:
- Designed to be easily unit-tested.
"""
from __future__ import annotations

from urllib.parse import quote_plus
from PyQt5.QtCore import QUrl

_GOOGLE_QUERY_URL = "https://www.google.com/search?q={query}"


def url_from_user_input(text: str) -> QUrl:
    """Convert a user string to a loadable QUrl.

    If *text* looks like a URL, ensure it has a scheme. Otherwise, treat it as a
    search query and return a Google search URL.

    Parameters
    ----------
    text : str
        Freeform user input from the address bar.

    Returns
    -------
    QUrl
        A fully qualified URL suitable for QWebEngineView.load().
    """
    text = (text or "").strip()
    if not text:
        return QUrl("https://www.google.com")

    url = QUrl.fromUserInput(text)

    # If QUrl already considers it a valid URL with a scheme, return as-is.
    if url.isValid() and url.scheme() and "." in url.host():
        return url

    # Heuristic: if it contains a dot and no spaces, treat as domain and add scheme if missing.
    if " " not in text and "." in text and "://" not in text:
        return QUrl(f"https://{text}")

    # Fallback to Google search.
    return QUrl(_GOOGLE_QUERY_URL.format(query=quote_plus(text)))
