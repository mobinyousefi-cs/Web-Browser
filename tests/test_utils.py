#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: tests/test_utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Unit tests for pure-Python utils (no GUI / Qt event loop required).
"""
from __future__ import annotations

from pyqt_web_browser.utils import url_from_user_input


def test_empty_defaults_to_google():
    url = url_from_user_input("")
    assert url.toString().startswith("https://www.google.")


def test_plain_domain_adds_scheme():
    url = url_from_user_input("example.com")
    assert url.toString() == "https://example.com"


def test_full_url_passes_through():
    url = url_from_user_input("https://www.python.org/")
    assert url.scheme() == "https"
    assert "python.org" in url.host()


def test_query_becomes_google_search():
    url = url_from_user_input("pyqt5 webengine tutorial")
    assert "google.com/search" in url.toString()
