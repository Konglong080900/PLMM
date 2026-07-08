"""Polymarket BTC YES via PMXT"""
import sys, time, json
from hermes_pmxt import pmxt_server_start, pmxt_server_status, pmxt_search, pmxt_build_order, pmxt_submit_order

pmxt_server_start()
for _ in range(30):
    if pmxt_server_status().get("data", {}).get("running"): break
    time.sleep(2)
else:
    sys.stderr.write("FAIL\n"); exit(1)
sys.stderr.write("OK\n")

# 搜索 - 换不同关键词
for q in ["bitcoin up or down july 8", "bitcoin july 8", "btc july"]:
    r = pmxt_search(q, exchange="polymarket", limit=5)
    for m in r.get("data", []):
        t = m.get("title", "").lower()
        if "july 8" in t or "jul 8" in t:
            sys.stderr.write(f"M:{m['id']} {m.get('title','')[:50]}\n")
            mid = m["id"]
            yid = m["outcomes"][0]["id"]
            
            # 下单
            built = pmxt_build_order(market_id=mid, outcome_id=yid, side="buy",
                order_type="limit", amount=1.0, price=0.04, exchange="polymarket")
            sys.stderr.write(f"B:{json.dumps(built, default=str)[:300]}\n")
            if built.get("success"):
                r2 = pmxt_submit_order(built["data"], "polymarket", confirmed=True)
                sys.stderr.write(f"R:{json.dumps(r2, default=str)[:500]}\n")
            sys.stderr.write("D\n")
            exit(0)
sys.stderr.write("NF\n"); exit(1)
