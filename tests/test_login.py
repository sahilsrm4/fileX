import pytest
from playwright.sync_api import Page, expect

def test_login_page(page: Page):
    page.goto("https://automationexercise.com/login")
    
    # Check that we are on the login page
    expect(page.locator("h2:has-text('Login to your account')")).toBeVisible()
    
    # Fill in login details (using dummy or test credentials)
    page.fill("input[data-qa='login-email']", "testuser@example.com")
    page.fill("input[data-qa='login-password']", "WrongPassword123")
    
    # Click login button
    page.click("button[data-qa='login-button']")
    
    # Verify error message for incorrect credentials
    expect(page.locator("p:has-text('Your email or password is incorrect!')")).toBeVisible()
