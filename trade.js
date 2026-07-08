const { ClobClient } = require('@polymarket/clob-client');

async function main() {
  const PK = process.env.PRIVATE_KEY;
  const AK = process.env.API_KEY;
  const YES_ID = '101163338685857975456381241657395646973932529603300193676223177504175672414916';

  console.log('🔑 API Key valid:', !!AK);
  console.log('🔑 PrivKey valid:', !!PK);

  // 尝试不同的构造方式
  try {
    const client = new ClobClient('https://clob.polymarket.com', 137, PK, AK);
    console.log('✅ Client created');

    console.log('\n🔄 下单买YES...');
    console.log('  token_id:', YES_ID);
    console.log('  price: 0.04');
    console.log('  size: 125');

    const result = await client.createAndPostOrder({
      tokenId: YES_ID,
      price: 0.04,
      size: 125,
      side: 'BUY',
    });

    console.log('\n✅ 成功!');
    console.log(JSON.stringify(result, null, 2).slice(0, 2000));
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    if (err.response?.data) console.error('响应:', JSON.stringify(err.response.data));
    if (err.stack) console.error(err.stack.split('\n').slice(0, 5).join('\n'));
    process.exit(1);
  }
}

main();
