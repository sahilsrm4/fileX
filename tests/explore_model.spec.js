const { test, expect } = require('@playwright/test');

test('Explore Models button test on watchguard.com', async ({ page }) => {
  // Navigate to WatchGuard home page
  await page.goto('https://www.watchguard.com');

  // Accept cookies if the cookie banner appears
  const acceptButton = page.locator('button:has-text(\'Accept All\')');
  if (await acceptButton.isVisible()) {
    await acceptButton.click();
  }

  // Locate and click the 'Explore Models' button/link
  const exploreModelsLink = page.locator('a:has-text(\'Explore Models\')').first();
  await exploreModelsLink.click();

  // Verify navigation to the rack-mount product page
  await expect(page).toHaveURL(/wgrd-products\/rack-mount/);
  await expect(page).toHaveTitle(/Rackmount Firewall Appliances/);
});
