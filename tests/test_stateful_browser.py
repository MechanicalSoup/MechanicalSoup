import mechanicalsoup


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://httpbin.org/")
    for link in browser.links():
        if link["href"] == "/":
            browser.follow_link(link)
            break
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

def test_no_404():
    browser = mechanicalsoup.StatefulBrowser()
    resp = browser.open("http://httpbin.org/nosuchpage")
    assert resp.status_code == 404

def test_404():
    browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
    try:
        resp = browser.open("http://httpbin.org/nosuchpage")
    except mechanicalsoup.LinkNotFoundError:
        pass
    else:
        assert False
    resp = browser.open("http://httpbin.org/")
    assert resp.status_code == 200

if __name__ == '__main__':
    test_submit_online()
    test_no_404()
    test_404()
