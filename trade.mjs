import { ClobClient } from "@polymarket/clob-client";
import { http, createWalletClient } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";

const PK = process.env.POLYMARKET_PRIVATE_KEY;
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";
const SAFE_ADDR = "0x39315cF2992D9dEeC20631976a236eE17D153521";

async function main() {
  const account = privateKeyToAccount(PK.startsWith("0x") ? PK : "0x" + PK);
  const walletClient = createWalletClient({ account, chain: polygon, transport: http() });

  // 先无cred初始化
  const client = new ClobClient("https://clob.polymarket.com", 137, walletClient, undefined, 2, SAFE_ADDR);
  
  // 尝试派生或创建API Key
  let creds;
  try {
    creds = await client.deriveApiKey();
    process.stderr.write("DERIVED\n");
  } catch {
    try {
      creds = await client.createApiKey();
      process.stderr.write("CREATED\n");
    } catch (e2) {
      process.stderr.write("NO_KEY:" + e2.message + "\n");
      // 用主人给的API Key
      creds = { apiKey: "019f40e6-91fa-72ac-a918-d9f474bf4872", secret: "", passphrase: "" };
    }
  }

  // 用creds重新创建client
  const authedClient = new ClobClient("https://clob.polymarket.com", 137, walletClient, creds, 2, SAFE_ADDR);
  process.stderr.write("READY\n");

  const order = await authedClient.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  process.stderr.write("SUCCESS\n");
  console.log(JSON.stringify(order));
}

main().catch(e => {
  process.stderr.write("ERR:" + (e.message || e) + "\n");
  if (e.response) process.stderr.write("RESP:" + JSON.stringify(e.response.data || {}) + "\n");
  if (e.stack) process.stderr.write("STACK:" + e.stack.split("\n").slice(0, 3).join("|") + "\n");
  process.exit(1);
});
