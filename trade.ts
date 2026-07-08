import { ClobClient } from "@polymarket/clob-client";

const PK = process.env.POLYMARKET_PRIVATE_KEY!;
const AK = process.env.POLYMARKET_API_KEY || "";
const YES_ID = "101163338685857975456381241657395646973932529603300193676223177504175672414916";

// 用ethers v6代替viem
const { ethers } = await import("ethers");
const wallet = new ethers.Wallet(PK.startsWith("0x") ? PK : `0x${PK}`);

// @polymarket/clob-client v5可用 Wallet 对象吗？
// 看看能不能直接传privateKey
try {
  const client = new ClobClient("https://clob.polymarket.com", 137, wallet);
  console.log("✅ Client ready");
  
  const order = await client.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  console.log("✅ Order:", JSON.stringify(order).slice(0, 1000));
} catch (e: any) {
  console.log("❌", e.message);
  // 换一种方式 - 直接用private key string
  const client2 = new ClobClient("https://clob.polymarket.com", 137, PK);
  console.log("✅ Client v2 ready");
  
  const order2 = await client2.createAndPostOrder({
    tokenID: YES_ID,
    price: 0.04,
    size: 25,
    side: "BUY",
  });
  console.log("✅ Order2:", JSON.stringify(order2).slice(0, 1000));
}
