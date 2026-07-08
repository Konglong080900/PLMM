"""
Polymarket Auto Trade - Buy BTC YES
"""
import os, json, sys
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs

PRIVATE_KEY = os.environ['PRIVATE_KEY']
API_KEY = os.environ['API_KEY']

print(f'🔑 API Key valid: {len(API_KEY) > 0}')
print(f'🔑 PrivKey valid: {len(PRIVATE_KEY) > 0}')

creds = ApiCreds(api_key=API_KEY, api_secret='', api_passphrase='')
YES_TOKEN_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916'

# 只试signature_type=0，不要循环
client = ClobClient(
    host='https://clob.polymarket.com',
    chain_id=137,
    key=PRIVATE_KEY,
    creds=creds,
    signature_type=0,
)

order_args = OrderArgs(
    token_id=YES_TOKEN_ID,
    price=0.04,
    size=125.0,
    side='BUY',
)

print(f'\\n🔄 创建并提交订单...')
print(f'  token_id={YES_TOKEN_ID}')
print(f'  price=0.04')
print(f'  size=125.0')
print(f'  side=BUY')

result = client.create_and_post_order(order_args)

print(f'\\n✅ 订单结果:')
print(json.dumps(result, indent=2, default=str)[:1000])

# 如果有order ID或transaction hash，打印出来
if isinstance(result, dict):
    order_id = result.get('order_id') or result.get('id') or result.get('orderId')
    if order_id:
        print(f'\\n🎯 订单ID: {order_id}')
    tx_hash = result.get('transaction_hash') or result.get('txHash')
    if tx_hash:
        print(f'🔗 交易哈希: {tx_hash}')

print('\\n完成!')
sys.exit(0)
