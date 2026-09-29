import pytest
from pages.watchguard_home_page import WatchGuardHomePage


@pytest.fixture
def home_page(page):
    page_obj = WatchGuardHomePage(page)
    page_obj.navigate()
    return page_obj


def test_button_english_language(home_page):
    home_page.click_button_by_name("English")


def test_button_platform(home_page):
    home_page.click_button_by_name("Platform")


def test_button_why_watchguard(home_page):
    home_page.click_button_by_name("Why WatchGuard")


def test_button_learn(home_page):
    home_page.click_button_by_name("Learn")


def test_button_company(home_page):
    home_page.click_button_by_name("Company")


def test_button_partners(home_page):
    home_page.click_button_by_name("Partners")


def test_button_support(home_page):
    home_page.click_button_by_name("Support")


def test_button_search_toggle(home_page):
    home_page.click_button_by_name("Search toggle")


def test_button_carousel_slide_1(home_page):
    home_page.click_button_by_name("More Power. Same Simplicity.")


def test_button_carousel_slide_2(home_page):
    home_page.click_button_by_name("Expose Hidden Cloud and Identity Threats")


def test_button_carousel_slide_3(home_page):
    home_page.click_button_by_name("Rai Never Sleeps. Stay Ahead.")


def test_button_carousel_slide_4(home_page):
    home_page.click_button_by_name("Endpoint Security Reimagined")


def test_button_pause(home_page):
    home_page.click_button_by_name("Pause")


def test_button_contact_us_form(home_page):
    home_page.click_button_by_name("Contact Us")


def test_button_carousel_next(home_page):
    home_page.click_button_by_name("Next")
