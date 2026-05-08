import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import monitor as _mon
from monitor import render_dashboard, run_monitor, REFRESH_INTERVAL

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DataMonitor - 주문 데이터 실시간 모니터")
    parser.add_argument("--once", action="store_true",
                        help="대시보드를 한 번만 출력하고 종료 (기본: 반복 갱신)")
    parser.add_argument("--interval", type=int, default=REFRESH_INTERVAL,
                        help=f"갱신 주기(초) (기본: {REFRESH_INTERVAL}초)")
    parser.add_argument("--path", type=str, default=None,
                        help="모니터링할 orders.json 경로 (환경변수 ORDER_DB_PATH 대신 사용)")
    args = parser.parse_args()

    if args.path:
        _mon.DB_PATH = args.path   # 런타임에 경로 덮어쓰기

    if args.once:
        orders = _mon.load_orders()
        render_dashboard(orders)
    else:
        run_monitor(interval=args.interval)
