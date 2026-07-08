import { ClobClient } from "@polymarket/clob-client";
import { http, createWalletClient } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";

const PK = process.env.POLYMARKET_PRIVATE_KEY;
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

try {
  const key = PK.startsWith("0x") ? PK : "0x" + PK;
  const account = privateKeyToAccount(key);
  const walletClient = createWalletClient({ account, chain: polygon, transport: http() });
  // 不传API Key，让SDK自动派生
  const client = new ClobClient("https://clob.polymarket.com", 137, walletClient, undefined, 0);
  console.log("✅ Client ready");

  const order = await client.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  console.log("✅ Order:", JSON.stringify(order).slice(0, 1000));
} catch (e) {
  console.log("❌", e.message);
  process.exit(1);
}
