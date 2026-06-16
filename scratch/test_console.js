const { chromium } = require('playwright-core');

(async () => {
  // Try to find the executable path dynamically, or use Edge/Chrome default path for windows
  const executablePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'; // common windows path
  
  try {
    const browser = await chromium.launch({ executablePath, headless: true });
    const page = await browser.newPage();
    
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error' || msg.type() === 'warning') {
        errors.push(`[${msg.type()}] ${msg.text()}`);
      }
    });

    page.on('pageerror', exception => {
      errors.push(`[pageerror] ${exception}`);
    });

    console.log("Navigating to http://localhost:3000/catalogo...");
    await page.goto('http://localhost:3000/catalogo', { waitUntil: 'networkidle' });
    
    await page.waitForTimeout(3000);

    if (errors.length > 0) {
      console.log("\n--- CONSOLE LOGS ---");
      errors.forEach(e => console.log(e));
    } else {
      console.log("\nNo errors detected.");
    }

    await browser.close();
  } catch(e) {
    console.error("Failed to launch browser:", e.message);
  }
})();
