from playwright.sync_api import Page

class WatchGuardHomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.watchguard.com")

    def click_button_by_name(self, name: str):
        self.page.get_by_role("button", name=name).click()

    def click_link_by_name(self, name: str):
        self.page.get_by_role("link", name=name).click()
