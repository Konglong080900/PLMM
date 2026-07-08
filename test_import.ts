console.log("Starting...");
try {
  const mod = await import("@polymarket/clob-client");
  console.log("Module keys:", Object.keys(mod));
} catch (e: any) {
  console.log("Import error:", e.message);
}
