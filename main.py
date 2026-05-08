import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from monitor import load_orders, render_dashboard, run_monitor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DataMonitor - 주문 데이터 실시간 모니터")
    parser.add_argument(
        "--once",
        action="store_true",
        help="대시보드를 한 번만 출력하고 종료 (기본: 반복 갱신)",
    )
    args = parser.parse_args()

    if args.once:
        orders = load_orders()
        render_dashboard(orders)
    else:
        run_monitor()
