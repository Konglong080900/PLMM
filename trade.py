"""
Polymarket Auto Trade via hermes-pmxt (PMXT sidecar)
"""
import os, sys, time
from hermes_pmxt import (
    pmxt_server_start, pmxt_server_status, pmxt_search,
    pmxt_quote, pmxt_build_order, pmxt_submit_order,
)

YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916"

# 启动sidecar
sys.stderr.write("Starting sidecar...\n")
pmxt_server_start()
for i in range(30):
    s = pmxt_server_status()
    if s.get("data", {}).get("running"):
        sys.stderr.write(f"SIDECAR_OK port={s['data']['port']}\n")
        break
    time.sleep(2)
else:
    sys.stderr.write("SIDECAR_FAIL\n")
    exit(1)

# 下单
sys.stderr.write("Placing order...\n")
built = pmxt_build_order(
    market_id=YES_ID,
    outcome="yes",
    side="buy",
    order_type="limit",
    amount=1.0,
    price=0.04,
    exchange="polymarket",
)
sys.stderr.write(f"BUILT:{built}\n")

result = pmxt_submit_order(built, "polymarket", confirmed=True)
sys.stderr.write(f"RESULT:{result}\n")
print(result)
