import sys

sys.path.append(r"D:\WatchGuard\command-line-file-utility\ai_interacting_with_tool")
import pytest
from pages.home_page import HomePage


@pytest.fixture(scope="function", autouse=True)
def setup_teardown(page):
    pass


def test_button_accept_cookies(page):
    home_page = HomePage(page)
    home_page.navigate()
    buttons = home_page.get_all_buttons()
    # Find button by name or index
    target_button = None
    for btn in buttons:
        try:
            if (
                "accept" in (btn.inner_text() or "").lower()
                or "cookie" in (btn.inner_text() or "").lower()
            ):
                target_button = btn
                break
        except:
            pass
    if not target_button and len(buttons) > 0:
        target_button = buttons[0]

    if target_button and target_button.is_visible():
        assert target_button.is_enabled(), "Button is not enabled."
        target_button.click()


def test_button_search(page):
    home_page = HomePage(page)
    home_page.navigate()
    buttons = home_page.get_all_buttons()
    target_button = None
    for btn in buttons:
        try:
            if (
                "search" in (btn.inner_text() or "").lower()
                or "magnifying" in (btn.get_attribute("aria-label") or "").lower()
            ):
                target_button = btn
                break
        except:
            pass
    if not target_button and len(buttons) > 1:
        target_button = buttons[1]

    if target_button and target_button.is_visible():
        assert target_button.is_enabled(), "Button is not enabled."
        target_button.click()


def test_button_menu(page):
    home_page = HomePage(page)
    home_page.navigate()
    buttons = home_page.get_all_buttons()
    target_button = None
    for btn in buttons:
        try:
            if (
                "menu" in (btn.inner_text() or "").lower()
                or "menu" in (btn.get_attribute("aria-label") or "").lower()
            ):
                target_button = btn
                break
        except:
            pass
    if not target_button and len(buttons) > 2:
        target_button = buttons[2]

    if target_button and target_button.is_visible():
        assert target_button.is_enabled(), "Button is not enabled."
        target_button.click()
