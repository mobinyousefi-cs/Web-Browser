#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: ui/main_window.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Main window with toolbar, tab bar, address bar, and wiring to BrowserTab widgets.

Usage:
from pyqt_web_browser.ui.main_window import MainWindow

Notes:
- Persists window geometry via QSettings under org 'mobinyousefi' / app 'pyqt-web-browser'.
"""
from __future__ import annotations

from typing import Optional

from PyQt5.QtCore import Qt, QSettings, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QStyle,
    QTabWidget,
    QToolBar,
    QWidget,
)

from pyqt_web_browser.browser import BrowserTab
from pyqt_web_browser.utils import url_from_user_input


HOMEPAGE = QUrl("https://www.google.com")


class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PyQt Web Browser")
        self.setMinimumSize(900, 640)

        self.settings = QSettings("mobinyousefi", "pyqt-web-browser")
        self._restore_geometry()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._current_tab_changed)
        self.setCentralWidget(self.tabs)

        self._init_toolbar()

        # Initial tab
        self.add_new_tab(HOMEPAGE, "New Tab")

    # --- UI setup ----------------------------------------------------------------------
    def _init_toolbar(self) -> None:
        tb = QToolBar("Navigation", self)
        tb.setIconSize(tb.iconSize())
        self.addToolBar(tb)

        style = self.style()
        icon_back = style.standardIcon(QStyle.SP_ArrowBack)
        icon_forward = style.standardIcon(QStyle.SP_ArrowForward)
        icon_reload = style.standardIcon(QStyle.SP_BrowserReload)
        icon_stop = style.standardIcon(QStyle.SP_BrowserStop)
        icon_home = style.standardIcon(QStyle.SP_DirHomeIcon)
        icon_newtab = style.standardIcon(QStyle.SP_FileDialogNewFolder)

        self.action_back = QAction(icon_back, "Back", self, triggered=self.navigate_back)
        self.action_forward = QAction(icon_forward, "Forward", self, triggered=self.navigate_forward)
        self.action_reload = QAction(icon_reload, "Reload", self, triggered=self.reload_page)
        self.action_stop = QAction(icon_stop, "Stop", self, triggered=self.stop_loading)
        self.action_home = QAction(icon_home, "Home", self, triggered=self.navigate_home)
        self.action_new_tab = QAction(icon_newtab, "New Tab", self, triggered=self.new_tab)

        tb.addActions([self.action_back, self.action_forward, self.action_reload, self.action_stop])
        tb.addSeparator()
        tb.addAction(self.action_home)
        tb.addSeparator()

        # Address bar
        addr_wrap = QWidget(self)
        addr_layout = QHBoxLayout(addr_wrap)
        addr_layout.setContentsMargins(0, 0, 0, 0)
        self.address_bar = QLineEdit(self)
        self.address_bar.setClearButtonEnabled(True)
        self.address_bar.returnPressed.connect(self._load_address_bar)
        addr_layout.addWidget(self.address_bar)
        tb.addWidget(addr_wrap)

        tb.addSeparator()
        tb.addAction(self.action_new_tab)

        # Shortcuts
        self.action_back.setShortcut(Qt.Key_Backspace)
        self.action_reload.setShortcut("Ctrl+R")
        self.action_home.setShortcut("Alt+Home")

    # --- Persistence -------------------------------------------------------------------
    def closeEvent(self, event) -> None:  # noqa: N802 (Qt signature)
        self._save_geometry()
        super().closeEvent(event)

    def _save_geometry(self) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def _restore_geometry(self) -> None:
        geom = self.settings.value("geometry")
        if geom is not None:
            self.restoreGeometry(geom)
        st = self.settings.value("windowState")
        if st is not None:
            self.restoreState(st)

    # --- Tabs --------------------------------------------------------------------------
    def add_new_tab(self, url: QUrl, label: str = "New Tab") -> None:
        tab = BrowserTab(url, self)
        i = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(i)

        # wire signals
        tab.titleChanged.connect(lambda title, i=i: self.tabs.setTabText(i, title[:30]))
        tab.iconChanged.connect(lambda icon, i=i: self.tabs.setTabIcon(i, QIcon(icon)))
        tab.urlChanged.connect(lambda u, i=i: self._update_address_bar(u, i))
        tab.loadProgress.connect(lambda p: self._update_reload_stop(p))

    def new_tab(self) -> None:
        self.add_new_tab(HOMEPAGE)

    def close_tab(self, index: int) -> None:
        if self.tabs.count() == 1:
            self.tabs.widget(index).deleteLater()
            self.close()
            return
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        widget.deleteLater()

    def _current_tab_changed(self, index: int) -> None:
        widget = self.tabs.widget(index)
        if isinstance(widget, BrowserTab):
            self._update_address_bar(widget.current_url(), index)
            self.setWindowTitle(widget.view.title() or "PyQt Web Browser")

    # --- Navigation --------------------------------------------------------------------
    def _load_address_bar(self) -> None:
        text = self.address_bar.text()
        url = url_from_user_input(text)
        self._current_tab().load(url)

    def _current_tab(self) -> BrowserTab:
        return self.tabs.currentWidget()  # type: ignore[return-value]

    def _update_address_bar(self, url: QUrl, index: int) -> None:
        if index == self.tabs.currentIndex():
            self.address_bar.blockSignals(True)
            self.address_bar.setText(url.toString())
            self.address_bar.blockSignals(False)

    def _update_reload_stop(self, progress: int) -> None:
        if progress < 100:
            self.action_reload.setVisible(False)
            self.action_stop.setVisible(True)
        else:
            self.action_stop.setVisible(False)
            self.action_reload.setVisible(True)

    def navigate_back(self) -> None:
        self._current_tab().back()

    def navigate_forward(self) -> None:
        self._current_tab().forward()

    def reload_page(self) -> None:
        self._current_tab().reload()

    def stop_loading(self) -> None:
        self._current_tab().stop()

    def navigate_home(self) -> None:
        self._current_tab().load(HOMEPAGE)
