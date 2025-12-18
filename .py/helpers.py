import os
import sys

"""
PyInstaller --onedir `
  --add-data "*.txt;res" `
  .\.py\application_handler.py
"""

def get_root_dir() -> str:
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))