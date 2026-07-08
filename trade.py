"""
Polymarket Auto Trade via hermes-pmxt
"""
import os, sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

# 启动sidecar
sys.stderr.write("Starting sidecar...\n")
pmxt_server_start()
for i in range(30):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write(f"SIDECAR_OK\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 搜索BTC市场获取outcome_id
sys.stderr.write("Searching market...\n")
m = pmxt_search("bitcoin up or down", exchange="polymarket", limit=5)
outcomes = m.get("data", [])
for o in outcomes:
    title = o.get("title", "")
    if "July 8" in title or "Jul 8" in title:
        yes_outcome_id = o["outcomes"][0]["id"]
        sys.stderr.write(f"FOUND:{yes_outcome_id}\n")
        break
else:
    sys.stderr.write("MARKET_NOT_FOUND\n")
    exit(1)

# 下单
sys.stderr.write("Building order...\n")
built = pmxt_build_order(
    market_id=yes_outcome_id,
    outcome="yes",
    side="buy",
    order_type="limit",
    amount=1.0,
    price=0.04,
    exchange="polymarket",
)
sys.stderr.write(f"BUILT:{json.dumps(built, default=str)[:200]}\n")

if built.get("success"):
    sys.stderr.write("Submitting...\n")
    result = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"RESULT:{json.dumps(result, default=str)[:500]}\n")
    print(result)

sys.stderr.write("DONE\n")
