import { ClobClient, Side } from "@polymarket/clob-client-v2";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";

const PK = process.env.POLYMARKET_PRIVATE_KEY!;
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";
const CONDITION_ID = "0x4b5f6236f5d1d037387555f61a76142a46812de8936dc700a939a9135fc321ce";

async function main() {
  const account = privateKeyToAccount(PK.startsWith("0x") ? PK : "0x" + PK);
  const signer = createWalletClient({ account, chain: { id: 137, name: "Polygon" }, transport: http() });

  // 1. 临时client获取API credentials
  const tempClient = new ClobClient({ host: "https://clob.polymarket.com", chain: 137, signer });
  const apiCreds = await tempClient.createOrDeriveApiKey();
  process.stderr.write("CREDS_OK\n");

  // 2. 正式client下单
  const client = new ClobClient({
    host: "https://clob.polymarket.com",
    chain: 137,
    signer,
    creds: apiCreds,
    signatureType: 0,  // EOA
    funderAddress: account.address,
  });

  // 3. 获取tick size和neg risk
  const market = await client.getMarket(CONDITION_ID);
  process.stderr.write("MARKET_OK\n");

  // 4. 下单
  const response = await client.createAndPostOrder(
    { tokenID: YES_ID, price: 0.04, size: 25, side: Side.BUY },
    { tickSize: String(market.minimum_tick_size), negRisk: market.neg_risk },
  );

  process.stderr.write("SUCCESS\n");
  console.log(JSON.stringify(response));
}

main().catch(e => {
  process.stderr.write("ERR:" + (e.message || e) + "\n");
  if (e.response) process.stderr.write("RESP:" + JSON.stringify(e.response.data || {}) + "\n");
  process.exit(1);
});
