class HomePage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.watchguard.com")

    def get_all_buttons(self):
        return self.page.get_by_role("button").all()
