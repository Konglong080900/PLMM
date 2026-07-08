const { ClobClient } = require('@polymarket/clob-client');

async function main() {
  const PRIVATE_KEY = process.env.PRIVATE_KEY;
  const API_KEY = process.env.API_KEY;
  const YES_TOKEN_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916';

  console.log('🔑 API Key valid:', !!API_KEY);
  console.log('🔑 PrivKey valid:', !!PRIVATE_KEY);

  const client = new ClobClient({
    host: 'https://clob.polymarket.com',
    chainId: 137,
    privateKey: PRIVATE_KEY,
    apiKey: API_KEY,
  });

  console.log('\n🔄 创建并提交订单...');
  console.log('  token_id:', YES_TOKEN_ID);
  console.log('  price: 0.04');
  console.log('  size: 125');
  console.log('  side: BUY');

  try {
    const result = await client.createAndPostOrder({
      tokenId: YES_TOKEN_ID,
      price: 0.04,
      size: 125,
      side: 'BUY',
    });
    console.log('\n✅ 成功!');
    console.log(JSON.stringify(result, null, 2).slice(0, 1000));
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    if (err.response) {
      console.error('  状态:', err.response.status);
      console.error('  响应:', JSON.stringify(err.response.data || {}));
    }
    process.exit(1);
  }
}

main();
