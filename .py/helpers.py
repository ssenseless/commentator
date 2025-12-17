import os
import sys


def get_cur_dir() -> str:
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.realpath(__file__))