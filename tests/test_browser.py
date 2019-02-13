import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import sys
from bs4 import BeautifulSoup
import tempfile
import os
from requests.cookies import RequestsCookieJar
import pytest


def test_submit_online(httpbin):
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get(httpbin + "/forms/post")
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


def test__request(httpbin):
    form_html = """
    <form method="post" action="{}/post">
      <input name="customer" value="Philip J. Fry"/>
      <input name="telephone" value="555"/>
      <textarea name="comments">freezer</textarea>
      <fieldset>
        <legend> Pizza Size </legend>
        <p><input type=RADIO name=size value="small">Small</p>
        <p><input type=radiO name=size value="medium" checked>Medium</p>
        <p><input type=radio name=size value="large">Large</p>
      </fieldset>
      <fieldset>
        <legend> Pizza Toppings </legend>
        <p><input type=CHECKBOX name="topping" value="bacon" checked>Bacon</p>
        <p><input type=checkBox name="topping" value="cheese">Extra Cheese</p>
        <p><input type=checkbox name="topping" value="onion" checked>Onion</p>
        <p><input type=checkbox name="topping" value="mushroom">Mushroom</p>
      </fieldset>
      <select name="shape">
        <option value="round">Round</option>
        <option value="square" selected>Square</option>
      </select>
    </form>
    """.format(httpbin.url)

    form = BeautifulSoup(form_html, "lxml").form

    browser = mechanicalsoup.Browser()
    response = browser._request(form)

    data = response.json()['form']
    assert data["customer"] == "Philip J. Fry"
    assert data["telephone"] == "555"
    assert data["comments"] == "freezer"
    assert data["size"] == "medium"
    assert data["topping"] == ["bacon", "onion"]
    assert data["shape"] == "square"

    assert "application/x-www-form-urlencoded" in response.request.headers[
        "Content-Type"]


@pytest.mark.parametrize('expected_content, set_value', [
    (b":-)", True),
    (b"", False)
])
def test__request_file(httpbin, expected_content, set_value):
    form_html = """
    <form method="post" action="{}/post">
      <input name="pic" type="file" />
    </form>
    """.format(httpbin.url)
    form = BeautifulSoup(form_html, "lxml").form

    if set_value:
        # create a temporary file for testing file upload
        pic_filedescriptor, pic_path = tempfile.mkstemp()
        os.write(pic_filedescriptor, expected_content)
        os.close(pic_filedescriptor)

        form.find("input", {"name": "pic"})["value"] = pic_path

    browser = mechanicalsoup.Browser()
    response = browser._request(form)

    # Check that only "files" includes a "pic" keyword in the response
    found = False
    for key, value in response.json().items():
        if key == "files":
            if "pic" in value:
                if value["pic"].encode() == expected_content:
                    # If pic is found twice, an error will occur
                    assert not found
                    found = True
        # One would expect to find "pic" in files, but as of writing,
        # httpbin puts it in form when the filename is empty:
        elif key == "form":
            if "pic" in value:
                if value["pic"].encode() == expected_content:
                    assert not found
                    found = True
                    assert b"filename=\"\"" in response.request.body
        else:
            assert (value is None) or ("pic" not in value)

    assert found
    assert "multipart/form-data" in response.request.headers["Content-Type"]

    # In case we created a file for upload, we need to close & delete it
    if set_value:
        os.remove(pic_path)


def test__request_select_none(httpbin):
    """Make sure that a <select> with no options selected
    submits the first option, as it does in a browser."""
    form_html = """
    <form method="post" action={}/post>
      <select name="shape">
        <option value="round">Round</option>
        <option value="square">Square</option>
      </select>
    </form>""".format(httpbin.url)

    form = BeautifulSoup(form_html, "lxml").form
    browser = mechanicalsoup.Browser()
    response = browser._request(form)
    assert response.json()['form'] == {'shape': 'round'}


def test__request_disabled_attr(httpbin):
    """Make sure that disabled form controls are not submitted."""
    form_html = """
    <form method="post" action="{}/post">
      <input disabled name="nosubmit" value="1" />
    </form>""".format(httpbin.url)

    browser = mechanicalsoup.Browser()
    response = browser._request(BeautifulSoup(form_html, "lxml").form)
    assert response.json()['form'] == {}


def test_no_404(httpbin):
    browser = mechanicalsoup.Browser()
    resp = browser.get(httpbin + "/nosuchpage")
    assert resp.status_code == 404


def test_404(httpbin):
    browser = mechanicalsoup.Browser(raise_on_404=True)
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        resp = browser.get(httpbin + "/nosuchpage")
    resp = browser.get(httpbin.url)
    assert resp.status_code == 200


def test_set_cookiejar(httpbin):
    """Set cookies locally and test that they are received remotely."""
    # construct a phony cookiejar and attach it to the session
    jar = RequestsCookieJar()
    jar.set('field', 'value')
    assert jar.get('field') == 'value'

    browser = mechanicalsoup.Browser()
    browser.set_cookiejar(jar)
    resp = browser.get(httpbin + "/cookies")
    assert resp.json() == {'cookies': {'field': 'value'}}


def test_get_cookiejar(httpbin):
    """Test that cookies set by the remote host update our session."""
    browser = mechanicalsoup.Browser()
    resp = browser.get(httpbin + "/cookies/set?k1=v1&k2=v2")
    assert resp.json() == {'cookies': {'k1': 'v1', 'k2': 'v2'}}

    jar = browser.get_cookiejar()
    assert jar.get('k1') == 'v1'
    assert jar.get('k2') == 'v2'


def test_post(httpbin):
    browser = mechanicalsoup.Browser()
    data = {'color': 'blue', 'colorblind': 'True'}
    resp = browser.post(httpbin + "/post", data)
    assert(resp.status_code == 200 and resp.json()['form'] == data)


if __name__ == '__main__':
    pytest.main(sys.argv)
