"""
Polymarket Auto Trade - hermes-pmxt
"""
import os, sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

# 启动sidecar
sys.stderr.write("Starting sidecar...\n")
pmxt_server_start()
for i in range(20):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write("SIDECAR_OK\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 搜索市场获取ID
sys.stderr.write("Searching...\n")
m = pmxt_search("bitcoin up or down on july 8 2026", exchange="polymarket", limit=5)
for o in m.get("data", []):
    t = o.get("title", "").lower()
    if "july 8" in t or "jul 8" in t:
        mid = o["id"]
        oid = o["outcomes"][0]["id"]
        sys.stderr.write(f"MATCH:{mid}|{oid}\n")
        break
else:
    sys.stderr.write("NOT_FOUND\n")
    exit(1)

# 下单 
sys.stderr.write("Ordering...\n")
built = pmxt_build_order(market_id=mid, outcome_id=oid, side="buy",
                          order_type="limit", amount=1.0, price=0.04,
                          exchange="polymarket")
sys.stderr.write(f"BUILT:{json.dumps(built, default=str)[:400]}\n")

if built.get("success"):
    result = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"RESULT:{json.dumps(result, default=str)[:500]}\n")
else:
    sys.stderr.write(f"FAIL:{built}\n")

sys.stderr.write("DONE\n")
