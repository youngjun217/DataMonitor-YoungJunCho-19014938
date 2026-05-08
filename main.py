import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from monitor import run_monitor

if __name__ == "__main__":
    run_monitor()
