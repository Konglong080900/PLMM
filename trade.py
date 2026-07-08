"""
Polymarket Auto Trade - debug
"""
import os, sys, time, json, subprocess
from hermes_pmxt import pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

# 直接启动pmxt server
sys.stderr.write("Starting pmxt server...\n")
proc = subprocess.Popen(
    ["python", "-m", "pmxt.server"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
)
time.sleep(3)
sys.stderr.write(f"PID={proc.pid}\n")

for i in range(20):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write("SIDECAR_OK\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 搜索并下单
sys.stderr.write("Searching...\n")
m = pmxt_search("bitcoin up or down july 8", exchange="polymarket", limit=5)
for o in m.get("data", []):
    if "july 8" in o.get("title","").lower():
        mid, oid = o["id"], o["outcomes"][0]["id"]
        sys.stderr.write(f"MATCH\n")
        break
else:
    sys.stderr.write("NOT_FOUND\n")
    exit(1)

sys.stderr.write("Ordering...\n")
built = pmxt_build_order(market_id=mid, outcome_id=oid, side="buy",
    order_type="limit", amount=1.0, price=0.04, exchange="polymarket")
sys.stderr.write(f"B:{json.dumps(built, default=str)[:400]}\n")
if built.get("success"):
    r = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
    sys.stderr.write(f"R:{json.dumps(r, default=str)[:500]}\n")
sys.stderr.write("DONE\n")
