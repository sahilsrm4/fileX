import pytest
from playwright.sync_api import Page, expect

def test_try_watchguard_cloud(page: Page):
    # Navigate to WatchGuard homepage
    page.goto("https://www.watchguard.com/")
    
    # Locate the 'Try WatchGuard Cloud Today' link and click it
    try_now_link = page.get_by_role("link", name="Try WatchGuard Cloud Today")
    expect(try_now_link).to_be_visible()
    try_now_link.click()
    
    # Verify that we navigated to the demos and free trials page
    expect(page).to_have_url("https://www.watchguard.com/wgrd-products/demos-free-trials?utm_source=Website&utm_term=WG-Cloud")
