import os, json, requests, time
from py_clob_client.client import ClobClient, order_to_json
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType

PK = os.environ['PRIVATE_KEY']
AK = os.environ['API_KEY']
YES_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916'

# 预测试代理列表
proxy_list = [
    'socks5://38.246.114.120:20202',
    'socks5://168.119.153.216:8888', 
    'socks5://50.205.246.13:8080',
    'http://38.246.114.120:20202',
    'http://168.119.153.216:8888',
    'http://50.205.246.13:8080',
    'socks5://209.97.172.125:1080',
    'http://34.134.231.117:3129',
]

# 找一个能用的代理
session = requests.Session()
proxy_found = False

for proxy in proxy_list:
    try:
        session.proxies = {'http': proxy, 'https': proxy}
        r = session.get('https://clob.polymarket.com/auth',
                       headers={'POLY_API_KEY': AK, 'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            print(f'代理 OK: {proxy}')
            proxy_found = True
            break
        elif r.status_code == 401:
            print(f'代理通(401): {proxy}')
            proxy_found = True
            break
    except:
        continue

if not proxy_found:
    print('无可用代理')
    exit(1)

# 创建签名订单
creds = ApiCreds(api_key=AK, api_secret='', api_passphrase='')
client = ClobClient(host='https://clob.polymarket.com', chain_id=137, key=PK, creds=creds)
order_args = OrderArgs(token_id=YES_ID, price=0.04, size=125.0, side='BUY')
signed = client.create_order(order_args)
body = order_to_json(signed, AK, OrderType.GTC)

# 下单
headers = {'POLY_API_KEY': AK, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
r = session.post('https://clob.polymarket.com/order', json=body, headers=headers, timeout=15)
print(f'HTTP {r.status_code}: {r.text[:200]}')

if r.status_code in [200, 201]:
    print('\n✅ 成功!')
    exit(0)

# 调整版本重试
if 'invalid order version' in r.text:
    body['order']['signatureType'] = 2
    body['order']['orderVersion'] = '2'
    r = session.post('https://clob.polymarket.com/order', json=body, headers=headers, timeout=15)
    print(f'重试 HTTP {r.status_code}: {r.text[:200]}')
    if r.status_code in [200, 201]:
        print('\n✅ 成功!')
        exit(0)

exit(1)
