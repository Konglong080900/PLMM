"""
Polymarket Auto Trade - hermes-pmxt
"""
import os, sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

# 启动sidecar
sys.stderr.write("Starting sidecar...\n")
r = pmxt_server_start()
sys.stderr.write(f"START:{json.dumps(r, default=str)[:100]}\n")

for i in range(20):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write("SIDECAR_OK\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 用outcome_id直接下单（YES token ID）
oid = "101163338685857975456381241657395646973932529603300193676223177504175672414916"
sys.stderr.write(f"Ordering {oid}...\n")

built = pmxt_build_order(
    outcome_id=oid, side="buy",
    order_type="limit", amount=1.0, price=0.04,
    exchange="polymarket",
)
sys.stderr.write(f"BUILT:{json.dumps(built, default=str)[:300]}\n")

if built.get("success"):
    result = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"RESULT:{json.dumps(result, default=str)[:500]}\n")
else:
    # 尝试用另一种方式
    built2 = pmxt_build_order(
        outcome_id=oid, outcome="yes", side="buy",
        order_type="limit", amount=1.0, price=0.04,
        exchange="polymarket",
    )
    sys.stderr.write(f"BUILT2:{json.dumps(built2, default=str)[:300]}\n")
    if built2.get("success"):
        result = pmxt_submit_order(built2["data"], "polymarket", confirmed=True)
        sys.stderr.write(f"RESULT2:{json.dumps(result, default=str)[:500]}\n")

sys.stderr.write("DONE\n")
