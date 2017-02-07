import mechanicalsoup


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://httpbin.org/")
    browser.follow_link("forms/post")
    assert browser.get_url() == "http://httpbin.org/forms/post"
    browser.select_form("form")
    browser["custname"] = "Customer Name Here"
    browser["size"] = "medium"
    browser["topping"] = ("cheese")
    browser["comments"] = "Some comment here"
    browser.get_current_form().set("nosuchfield", "new value", True)
    response = browser.submit_selected()
    json = response.json()
    data = json["form"]
    assert data["custname"] == "Customer Name Here"
    assert data["custtel"] == ""  # web browser submits "" for input left blank
    assert data["size"] == "medium"
    assert data["topping"] == "cheese"
    assert data["comments"] == "Some comment here"
    assert data["nosuchfield"] == "new value"


if __name__ == '__main__':
    test_submit_online()
