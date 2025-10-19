#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: PyQt Web Browser
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
CLI entrypoint to launch the PyQt Web Browser application.

Usage:
python -m pyqt_web_browser

Notes:
- Also registered as a console script `pyqt-web-browser` in pyproject.toml.
"""
from __future__ import annotations

import sys
from pyqt_web_browser.app import create_app


def main() -> int:
    app, _window = create_app()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
