import mechanicalsoup


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = mechanicalsoup.Form(page.soup.form)

    input_data = {"custname": "Philip J. Fry"}
    form.input(input_data)

    check_data = {"size": "medium", "topping": ["cheese", "onion"]}
    form.check(check_data)

    form.textarea({"comments": "warm"})
    form.textarea({"comments": "actually, no, not warm"})
    form.textarea({"comments": "freezer"})

    response = browser.submit(form, page.url)

    # helpfully the form submits to http://httpbin.org/post which simply
    # returns the request headers in json format
    json = response.json()
    data = json["form"]
    assert data["custname"] == "Philip J. Fry"
    assert data["custtel"] == ""  # web browser submits "" for input left blank
    assert data["size"] == "medium"
    assert data["topping"] == ["cheese", "onion"]
    assert data["comments"] == "freezer"

if __name__ == '__main__':
    test_submit_online()
