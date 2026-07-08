"""
Polymarket Auto Trade - Buy BTC Up or Down July 8 YES
"""
import os
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs

PRIVATE_KEY = os.environ['PRIVATE_KEY']
API_KEY = os.environ['API_KEY']

creds = ApiCreds(api_key=API_KEY, api_secret='', api_passphrase='')

# 尝试不同的signature_type
for sig_type in [0, 1, 2]:
    try:
        client = ClobClient(
            host='https://clob.polymarket.com',
            chain_id=137,
            key=PRIVATE_KEY,
            creds=creds,
            signature_type=sig_type,
        )
        
        YES_TOKEN_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916'
        order_args = OrderArgs(
            token_id=YES_TOKEN_ID,
            price=0.04,
            size=125.0,
            side='BUY',
        )
        
        print(f'🔄 尝试 signature_type={sig_type}...')
        result = client.create_and_post_order(order_args)
        print(f'✅ 成功! {result}')
        break
    except Exception as e:
        err = str(e)
        if 'invalid order version' in err:
            print(f'  ❌ 版本错误，继续尝试...')
        elif 'balance' in err.lower() or 'allowance' in err.lower():
            print(f'  ❌ 余额/授权问题: {err[:100]}')
        else:
            print(f'  ❌ {err[:100]}')
