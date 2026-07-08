"""
Polymarket Auto Trade - Buy BTC Up or Down July 8 YES
"""
import os
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs

PRIVATE_KEY = os.environ['PRIVATE_KEY']
API_KEY = os.environ['API_KEY']

creds = ApiCreds(api_key=API_KEY, api_secret='', api_passphrase='')
client = ClobClient(
    host='https://clob.polymarket.com',
    chain_id=137,
    key=PRIVATE_KEY,
    creds=creds,
)

YES_TOKEN_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916'

# 花5 USDC买YES @ 0.04
order_args = OrderArgs(
    token_id=YES_TOKEN_ID,
    price=0.04,
    size=125.0,
    side='BUY',
)

print('🔄 创建并提交订单...')
result = client.create_and_post_order(order_args)
print(f'✅ 成功! {result}')
