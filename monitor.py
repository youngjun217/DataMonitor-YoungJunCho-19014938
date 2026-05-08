import json
import os
import time
import unicodedata
from collections import Counter
from datetime import datetime
from typing import List


def _dw(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)

def _ljust(s: str, w: int) -> str:
    return s + " " * max(0, w - _dw(s))

def _rjust(s: str, w: int) -> str:
    return " " * max(0, w - _dw(s)) + s


DB_PATH = os.environ.get("ORDER_DB_PATH", "data/orders.json")
REFRESH_INTERVAL = int(os.environ.get("MONITOR_INTERVAL", "3"))

# SampleOrderSystem 상태코드 기준
STATUSES = ["RESERVED", "PRODUCING", "CONFIRMED", "RELEASE", "REJECTED"]


def load_orders() -> List[dict]:
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_dashboard(orders: List[dict]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(orders)
    status_counts = Counter(o.get("status", "unknown") for o in orders)
    released = sum(1 for o in orders if o.get("status") == "RELEASE")

    print("=" * 70)
    print(f"  ORDER DATA MONITOR  |  {now}  |  DB: {DB_PATH}")
    print("=" * 70)

    print(f"\n  [요약]")
    print(f"    총 주문     : {total}건")
    print(f"    출고 완료   : {released}건")

    print(f"\n  [상태별 현황]")
    for s in STATUSES:
        count = status_counts.get(s, 0)
        pct = (count / total * 100) if total else 0
        filled = min(count, 20)
        bar = "#" * filled + "-" * (20 - filled)
        print(f"    {s:<12} |{bar}|  {count:>3}건  ({pct:4.1f}%)")

    print(f"\n  [최근 주문 5건]")
    if not orders:
        print("    데이터 없음")
    else:
        recent = sorted(orders, key=lambda o: o.get("created_at", ""), reverse=True)[:5]
        print("    " + _ljust("ID", 10) + " " + _ljust("고객명", 16) + " " +
              _ljust("상태", 12) + " " + _rjust("수량", 5) + "  납기일")
        print("    " + "-" * 60)
        for o in recent:
            print(
                "    " + _ljust(o["id"], 10) + " " +
                _ljust(o.get("customer_name", ""), 16) + " " +
                _ljust(o.get("status", "?"), 12) + " " +
                _rjust(f"{o.get('quantity', 0)}개", 5) + "  " +
                o.get("due_date", "")
            )

    print(f"\n  갱신 주기: {REFRESH_INTERVAL}초  |  Ctrl+C 로 종료")
    print("=" * 70)


def run_monitor(interval: int = REFRESH_INTERVAL) -> None:
    print(f"DataMonitor 시작 (DB: {DB_PATH}, 갱신: {interval}초)")
    try:
        while True:
            orders = load_orders()
            clear_screen()
            render_dashboard(orders)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n모니터 종료.")
