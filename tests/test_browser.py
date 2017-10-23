import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import sys
from bs4 import BeautifulSoup
import tempfile
from requests.cookies import RequestsCookieJar
import pytest


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = page.soup.form

    form.find("input", {"name": "custname"})["value"] = "Philip J. Fry"
    # leave custtel blank without value
    assert "value" not in form.find("input", {"name": "custtel"}).attrs
    form.find("input", {"name": "size", "value": "medium"})["checked"] = ""
    form.find("input", {"name": "topping", "value": "cheese"})["checked"] = ""
    form.find("input", {"name": "topping", "value": "onion"})["checked"] = ""
    form.find("textarea", {"name": "comments"}).insert(0, "freezer")

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

    assert json["headers"]["User-Agent"].startswith('python-requests/')
    assert 'MechanicalSoup' in json["headers"]["User-Agent"]
    browser.close()


form_html = """
<form method="post" action="http://httpbin.org/post">
<input name="customer" value="Philip J. Fry"/>
<input name="telephone" value="555"/>
<textarea name="comments">freezer</textarea>
<fieldset>
 <legend> Pizza Size </legend>
 <p><input type=radio name=size value="small">Small</p>
 <p><input type=radio name=size value="medium" checked>Medium</p>
 <p><input type=radio name=size value="large">Large</p>
</fieldset>
<fieldset>
 <legend> Pizza Toppings </legend>
 <p><input type=checkbox name="topping" value="bacon">Bacon</p>
 <p><input type=checkbox name="topping" value="cheese" checked>Extra Cheese</p>
 <p><input type=checkbox name="topping" value="onion" checked>Onion</p>
 <p><input type=checkbox name="topping" value="mushroom">Mushroom</p>
</fieldset>
<input name="pic" type="file">
<select name="shape">
 <option value="round">Round</option>
 <option value="square" selected>Square</option>
</select>
"""


def test_build_request():
    form = BeautifulSoup(form_html, "lxml").form

    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)

    assert request.data["customer"] == "Philip J. Fry"
    assert request.data["telephone"] == "555"
    assert request.data["comments"] == "freezer"
    assert request.data["size"] == "medium"
    assert request.data["topping"] == ["cheese", "onion"]
    assert request.data["shape"] == "square"

    request = browser._prepare_request(form)
    assert "application/x-www-form-urlencoded" in request.headers[
        "Content-Type"]
    browser.close()


def test_prepare_request_file():
    form = BeautifulSoup(form_html, "lxml").form

    # create a temporary file for testing file upload
    pic_path = tempfile.mkstemp()[1]
    with open(pic_path, "w") as f:
        f.write(":-)")

    form.find("input", {"name": "pic"})["value"] = pic_path

    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)

    assert request.files
    assert request.files["pic"]
    assert request.files["pic"].read() == ":-)".encode("utf8")
    assert "pic" not in request.data

    request = browser._prepare_request(form)
    assert "multipart/form-data" in request.headers["Content-Type"]
    browser.close()


def test_no_404():
    browser = mechanicalsoup.Browser()
    resp = browser.get("http://httpbin.org/nosuchpage")
    assert resp.status_code == 404
    browser.close()


def test_404():
    browser = mechanicalsoup.Browser(raise_on_404=True)
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        resp = browser.get("http://httpbin.org/nosuchpage")
    resp = browser.get("http://httpbin.org/")
    assert resp.status_code == 200
    browser.close()


def test_set_cookiejar():
    """Set cookies locally and test that they are received remotely."""
    # construct a phony cookiejar and attach it to the session
    jar = RequestsCookieJar()
    jar.set('field', 'value')
    assert jar.get('field') == 'value'

    browser = mechanicalsoup.Browser()
    browser.set_cookiejar(jar)
    resp = browser.get("http://httpbin.org/cookies")
    assert resp.json() == {'cookies': {'field': 'value'}}
    browser.close()


def test_get_cookiejar():
    """Test that cookies set by the remote host update our session."""
    browser = mechanicalsoup.Browser()
    resp = browser.get("http://httpbin.org/cookies/set?k1=v1&k2=v2")
    assert resp.json() == {'cookies': {'k1': 'v1', 'k2': 'v2'}}

    jar = browser.get_cookiejar()
    assert jar.get('k1') == 'v1'
    assert jar.get('k2') == 'v2'
    browser.close()


def test_post():
    browser = mechanicalsoup.Browser()
    data = {'color': 'blue', 'colorblind': 'True'}
    resp = browser.post("http://httpbin.org/post", data)
    assert(resp.status_code == 200 and resp.json()['form'] == data)
    browser.close()


if __name__ == '__main__':
    pytest.main(sys.argv)
