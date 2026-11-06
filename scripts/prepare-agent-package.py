#!/usr/bin/env python3
"""Backward-compatible entry point for building agent distributions."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("build-distributions.py")), run_name="__main__")
