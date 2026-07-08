"""
Polymarket Auto Trade - BTC YES via Tor proxy
"""
import os, sys
from py_clob_client_v2 import ClobClient, OrderArgs, SignatureTypeV2
from py_clob_client_v2.order_builder.constants import BUY
from py_clob_client_v2.clob_types import PartialCreateOrderOptions, OrderType

PK = os.environ['POLYMARKET_PRIVATE_KEY']
YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916"

try:
    tmp = ClobClient("https://clob.polymarket.com", key=PK, chain_id=137)
    creds = tmp.create_or_derive_api_key()
    sys.stderr.write("CREDS_OK\n")
except Exception as e:
    sys.stderr.write(f"CREDS_ERR:{e}\n")
    from py_clob_client_v2.clob_types import ApiCreds
    creds = ApiCreds(api_key="019f40e6-91fa-72ac-a918-d9f474bf4872", api_secret="", api_passphrase="")

client = ClobClient(
    "https://clob.polymarket.com", key=PK, chain_id=137,
    creds=creds, signature_type=SignatureTypeV2.POLY_1271,
    funder="0x3f093615A38D5B2994dF467b3E70085046333870",
)
sys.stderr.write("CLIENT_OK\n")

market = client.get_market("0x4b5f6236f5d1d037387555f61a76142a46812de8936dc700a939a9135fc321ce")
sys.stderr.write(f"MARKET_OK tick={market['minimum_tick_size']}\n")

resp = client.create_and_post_order(
    OrderArgs(token_id=YES_ID, price=0.04, size=25, side=BUY),
    options=PartialCreateOrderOptions(tick_size=str(market['minimum_tick_size']), neg_risk=market['neg_risk']),
    order_type=OrderType.GTC,
)
sys.stderr.write("SUCCESS\n")
print(resp)
