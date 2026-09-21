const { test, expect } = require('@playwright/test');

test('User can login successfully', async ({ page }) => {
  await page.goto('https://automationexercise.com/login');
  
  // Verify login section is visible
  await expect(page.getByRole('heading', { name: 'Login to your account' })).toBeVisible();
  
  // Fill in login credentials
  await page.getByRole('textbox', { name: 'Email Address' }).first().fill('testuser@example.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password123');
  
  // Click login button
  await page.getByRole('button', { name: 'Login' }).click();
});
