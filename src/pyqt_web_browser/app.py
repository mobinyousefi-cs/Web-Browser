#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: app.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Application factory for the browser, responsible for creating the QApplication
and the main window.

Usage:
from pyqt_web_browser.app import create_app

Notes:
- Keeps main entry light and importable for unit testing.
"""
from __future__ import annotations

import sys
from PyQt5.QtWidgets import QApplication
from pyqt_web_browser.ui.main_window import MainWindow


def create_app(argv: list[str] | None = None) -> tuple[QApplication, MainWindow]:
    """Create and initialize the QApplication and main window.

    Parameters
    ----------
    argv : list[str] | None
        Command line arguments (defaults to sys.argv).

    Returns
    -------
    (QApplication, MainWindow)
    """
    argv = list(sys.argv if argv is None else argv)

    app = QApplication(argv)
    app.setApplicationName("pyqt-web-browser")
    app.setOrganizationName("mobinyousefi")
    app.setOrganizationDomain("github.com/mobinyousefi-cs")

    window = MainWindow()
    window.show()
    return app, window
