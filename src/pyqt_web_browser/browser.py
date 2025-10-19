#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: browser.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Browser tab widget wrapping QWebEngineView with a small API to connect UI controls.

Usage:
Used by MainWindow to create and manage tabs.

Notes:
- Provides helpers for navigation, loading, and title/url propagation via signals.
"""
from __future__ import annotations

from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class BrowserTab(QWidget):
    titleChanged = pyqtSignal(str)
    urlChanged = pyqtSignal(QUrl)
    iconChanged = pyqtSignal(object)
    loadProgress = pyqtSignal(int)

    def __init__(self, url: QUrl, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.view = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        # Wire signals to re-emit at the tab-level
        self.view.titleChanged.connect(self.titleChanged)
        self.view.urlChanged.connect(self.urlChanged)
        self.view.iconChanged.connect(self.iconChanged)
        self.view.loadProgress.connect(self.loadProgress)

        if url.isValid():
            self.view.load(url)

    # Navigation API
    def back(self) -> None:
        self.view.back()

    def forward(self) -> None:
        self.view.forward()

    def reload(self) -> None:
        self.view.reload()

    def stop(self) -> None:
        self.view.stop()

    def load(self, url: QUrl) -> None:
        self.view.load(url)

    def zoom_in(self) -> None:
        self.view.setZoomFactor(self.view.zoomFactor() + 0.1)

    def zoom_out(self) -> None:
        self.view.setZoomFactor(self.view.zoomFactor() - 0.1)

    def zoom_reset(self) -> None:
        self.view.setZoomFactor(1.0)

    def find_in_page(self, text: str) -> None:
        self.view.findText(text)

    def current_url(self) -> QUrl:
        return self.view.url()
