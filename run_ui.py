"""Streamlit entry point. Run from project root: streamlit run run_ui.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import trading_bot.bot.ui  # noqa: F401
