def test_example(page):
    page.goto("https://example.com")
    assert "Example Domain" in page.title()
