"""
Polymarket Auto Trade - hermes-pmxt
"""
import os, sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

pmxt_server_start()
for i in range(20):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"): break
    time.sleep(2)
else:
    sys.stderr.write("FAIL\n"); exit(1)

sys.stderr.write("OK\n")

# 搜索市场
m = pmxt_search("bitcoin up or down on july 8", exchange="polymarket", limit=5)
for o in m.get("data", []):
    if "july 8" in o.get("title","").lower():
        mid, oid = o["id"], o["outcomes"][0]["id"]
        sys.stderr.write(f"M\n")
        break
else:
    sys.stderr.write("NF\n"); exit(1)

# 下单
built = pmxt_build_order(market_id=mid, outcome_id=oid, side="buy",
    order_type="limit", amount=1.0, price=0.04, exchange="polymarket")
sys.stderr.write(f"B:{json.dumps(built, default=str)[:300]}\n")

if built.get("success"):
    r = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"R:{json.dumps(r, default=str)[:500]}\n")
sys.stderr.write("D\n")
