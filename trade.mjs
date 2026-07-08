import { ClobClient } from "@polymarket/clob-client";
import { http, createWalletClient } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";

const PK = process.env.POLYMARKET_PRIVATE_KEY;
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

// 临时写死API Key测试
const AK = "019f40e6-91fa-72ac-a918-d9f474bf4872";

try {
  const account = privateKeyToAccount(PK.startsWith("0x") ? PK : "0x" + PK);
  const walletClient = createWalletClient({ account, chain: polygon, transport: http() });
  const client = new ClobClient("https://clob.polymarket.com", 137, walletClient, { key: AK, secret: "", passphrase: "" }, 0);
  process.stderr.write("READY\n");

  const order = await client.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  process.stderr.write("SUCCESS\n");
  console.log(JSON.stringify(order));
} catch (e) {
  process.stderr.write("ERR:" + (e.message || e) + "\n");
  if (e.response) process.stderr.write("RESP:" + JSON.stringify(e.response.data || {}) + "\n");
  if (e.stack) process.stderr.write("STACK:" + e.stack.split("\n").slice(0, 3).join("|") + "\n");
  process.exit(1);
}
