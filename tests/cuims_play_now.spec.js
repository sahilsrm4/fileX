const { test, expect } = require('@playwright/test');

test('Verify CUIMS Play Now button', async ({ page }) => {
  await page.goto('https://www.cuims.org/');
  const playNowButton = page.locator('link', { hasText: 'Play Now' });
  await expect(playNowButton).toBeVisible();
  await playNowButton.click();
  await expect(page).toHaveURL(/services/);
});
