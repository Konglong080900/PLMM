"""Polymarket BTC YES via PMXT"""
import sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

pmxt_server_start()
for _ in range(30):
    if pmxt_server_status().get("data", {}).get("running"): break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n"); exit(1)
sys.stderr.write("OK\n")

# 搜市场 - 用slug精确匹配
r = pmxt_search("bitcoin-up-or-down-on-july-8", exchange="polymarket", limit=3)
for m in r.get("data", []):
    if "july 8" in m.get("title", "").lower():
        mid = m["id"]
        sys.stderr.write(f"M:{mid}\n")
        break
else:
    sys.stderr.write("NF\n"); exit(1)

# 下单（用outcome="yes"而不是outcome_id）
built = pmxt_build_order(market_id=mid, outcome="yes", side="buy",
    order_type="limit", amount=1.0, price=0.04, exchange="polymarket")
sys.stderr.write(f"B:{json.dumps(built, default=str)[:300]}\n")

if built.get("success"):
    r2 = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"R:{json.dumps(r2, default=str)[:500]}\n")
sys.stderr.write("D\n")
