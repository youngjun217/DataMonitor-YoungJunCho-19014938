import json
import os
import time
from collections import Counter
from datetime import datetime
from typing import List


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
        filled = min(count, 20)
        bar = "#" * filled + "-" * (20 - filled)
        print(f"    {s:<12} |{bar}|  {count}건")

    print(f"\n  [최근 주문 5건]")
    if not orders:
        print("    데이터 없음")
    else:
        recent = sorted(orders, key=lambda o: o.get("created_at", ""), reverse=True)[:5]
        print(f"    {'ID':<10} {'고객명':<15} {'상태':<12} {'수량':>5}  {'납기일'}")
        print("    " + "-" * 57)
        for o in recent:
            print(
                f"    {o['id']:<10} {o['customer_name']:<15} "
                f"{o.get('status', '?'):<12} "
                f"{o.get('quantity', 0):>5}개  "
                f"{o.get('due_date', '')}"
            )

    print(f"\n  갱신 주기: {REFRESH_INTERVAL}초  |  Ctrl+C 로 종료")
    print("=" * 70)


def run_monitor() -> None:
    print(f"DataMonitor 시작 (DB: {DB_PATH}, 갱신: {REFRESH_INTERVAL}초)")
    try:
        while True:
            orders = load_orders()
            clear_screen()
            render_dashboard(orders)
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\n모니터 종료.")
