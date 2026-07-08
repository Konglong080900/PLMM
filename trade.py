import os, json, requests, time
from py_clob_client.client import ClobClient, order_to_json
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType

PK = os.environ['PRIVATE_KEY']
AK = os.environ['API_KEY']
YES_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916'

session = requests.Session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:19050',
    'https': 'socks5h://127.0.0.1:19050',
}

# 等待Tor就绪
for i in range(12):
    try:
        ip = session.get('https://httpbin.org/ip', timeout=5).json()
        print('Tor出口:', ip.get('origin', '?'))
        break
    except:
        if i == 0:
            print('等待Tor启动...', end='', flush=True)
        else:
            print('.', end='', flush=True)
        time.sleep(5)
else:
    print('\nTor未就绪')
    exit(1)

print('\nTor就绪!')

# 创建并签名订单
creds = ApiCreds(api_key=AK, api_secret='', api_passphrase='')
client = ClobClient(host='https://clob.polymarket.com', chain_id=137, key=PK, creds=creds)
order_args = OrderArgs(token_id=YES_ID, price=0.04, size=125.0, side='BUY')
signed = client.create_order(order_args)
body = order_to_json(signed, AK, OrderType.GTC)

print('下单中...')
try:
    r = session.post('https://clob.polymarket.com/order', json=body,
        headers={'POLY_API_KEY': AK, 'Content-Type': 'application/json'}, timeout=30)
    print(f'HTTP {r.status_code}:', r.text[:300])
    if r.status_code in [200, 201]:
        print('\n✅ 成功!')
        exit(0)
    elif 'invalid order version' in r.text:
        print('\n版本问题，尝试调整...')
        body['order']['signatureType'] = 2
        body['order']['orderVersion'] = '2'
        r = session.post('https://clob.polymarket.com/order', json=body,
            headers={'POLY_API_KEY': AK, 'Content-Type': 'application/json'}, timeout=30)
        print(f'重试 HTTP {r.status_code}:', r.text[:300])
        if r.status_code in [200, 201]:
            print('\n✅ 成功!')
            exit(0)
except Exception as e:
    print('错误:', str(e)[:100])

exit(1)
