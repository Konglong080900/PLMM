import os, json, requests
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

try:
    ip = session.get('https://httpbin.org/ip', timeout=15).json()
    print('Tor出口:', ip.get('origin', '?'))
except:
    print('Tor未就绪')
    exit(1)

creds = ApiCreds(api_key=AK, api_secret='', api_passphrase='')
client = ClobClient(host='https://clob.polymarket.com', chain_id=137, key=PK, creds=creds)
order_args = OrderArgs(token_id=YES_ID, price=0.04, size=125.0, side='BUY')
signed = client.create_order(order_args)
body = order_to_json(signed, AK, OrderType.GTC)

for sig_val in [0, 2]:
    for ver in [None, '2', '1.0.0']:
        b = json.loads(json.dumps(body, default=str))
        b['order']['signatureType'] = sig_val
        if ver:
            b['order']['orderVersion'] = ver

        tag = f'sigType={sig_val} ver={ver}'
        print(f'Trying {tag}...')

        try:
            r = session.post('https://clob.polymarket.com/order', json=b,
                headers={'POLY_API_KEY': AK, 'Content-Type': 'application/json'}, timeout=15)
            print(f'  HTTP {r.status_code}: {r.text[:200]}')
            if r.status_code in [200, 201]:
                print('SUCCESS!', r.text[:500])
                exit(0)
        except Exception as e:
            print(f'  Error: {str(e)[:60]}')

print('All failed')
exit(1)
