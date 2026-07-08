"""
Polymarket Auto Trade via hermes-pmxt
"""
import os, sys, time, json, subprocess
from hermes_pmxt import pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

# 手动启动sidecar (用npx)
sys.stderr.write("Starting sidecar...\n")
proc = subprocess.Popen(
    ["npx", "--yes", "pmxt", "server", "--port", "3847"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

for i in range(30):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write("SIDECAR_OK\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 搜索市场
sys.stderr.write("Searching...\n")
m = pmxt_search("bitcoin up or down july 8", exchange="polymarket", limit=5)
for o in m.get("data", []):
    t = o.get("title", "")
    if "july 8" in t.lower() or "jul 8" in t.lower():
        oid = o["outcomes"][0]["id"]
        sys.stderr.write(f"FOUND:{oid}\n")
        break
else:
    sys.stderr.write("NOT_FOUND\n")
    exit(1)

# 下单
sys.stderr.write("Ordering...\n")
built = pmxt_build_order(market_id=oid, outcome="yes", side="buy",
                          order_type="limit", amount=1.0, price=0.04,
                          exchange="polymarket")
sys.stderr.write(f"BUILT:{json.dumps(built, default=str)[:300]}\n")

if built.get("success"):
    result = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"RESULT:{json.dumps(result, default=str)[:500]}\n")
    print(result)
sys.stderr.write("DONE\n")
