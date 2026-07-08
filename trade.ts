import { ClobClient } from "@polymarket/clob-client";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";

const PK = process.env.POLYMARKET_PRIVATE_KEY!;
const AK = process.env.POLYMARKET_API_KEY || "";
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

const account = privateKeyToAccount(PK as `0x${string}`);
const walletClient = createWalletClient({ account, chain: polygon, transport: http() });

// 传API Key
const creds = AK ? { key: AK, secret: "", passphrase: "" } : undefined;
const client = new ClobClient("https://clob.polymarket.com", 137, walletClient, creds, 0);

console.log("✅ Client ready, placing order...");

// 用正确的参数名: tokenID (大写D), side 大写
const order = await client.createAndPostOrder({
  tokenID: YES_ID,
  price: 0.04,
  size: 25,   // 1 USDC = 25个YES @ 0.04
  side: "BUY",
});

console.log("✅ Order placed:", JSON.stringify(order).slice(0, 1000));
