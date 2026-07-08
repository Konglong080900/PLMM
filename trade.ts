import { ClobClient } from "@polymarket/clob-client";

const PK = process.env.POLYMARKET_PRIVATE_KEY!;
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

const client = new ClobClient("https://clob.polymarket.com", 137, PK);
console.log("✅ Client created");

const order = await client.createAndPostOrder({
  tokenId: YES_ID,
  price: 0.04,
  size: 125,
  side: "BUY",
});

console.log("✅ Order placed:", JSON.stringify(order));
