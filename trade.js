const { ClobClient } = require("@polymarket/clob-client");
const { http, createWalletClient } = require("viem");
const { privateKeyToAccount } = require("viem/accounts");
const { polygon } = require("viem/chains");

const PK = process.env.POLYMARKET_PRIVATE_KEY;
const AK = process.env.POLYMARKET_API_KEY || "";
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

async function main() {
  const key = PK.startsWith("0x") ? PK : "0x" + PK;
  const account = privateKeyToAccount(key);
  const walletClient = createWalletClient({ account, chain: polygon, transport: http() });
  const creds = AK ? { key: AK, secret: "", passphrase: "" } : undefined;
  const client = new ClobClient("https://clob.polymarket.com", 137, walletClient, creds, 0);

  console.log("✅ Client ready");
  const order = await client.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  console.log("✅ Order:", JSON.stringify(order).slice(0, 1000));
}

main().catch(e => {
  console.log("❌", e.message);
  if (e.stack) console.log(e.stack.split("\n").slice(0, 3).join("\n"));
  process.exit(1);
});
