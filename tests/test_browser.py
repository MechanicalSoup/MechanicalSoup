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


valid_enctypes_file_submit = {"multipart/form-data": True,
                              "application/x-www-form-urlencoded": False
                              }

default_enctype = "application/x-www-form-urlencoded"


@pytest.mark.parametrize("file_field", [
  """<input name="pic" type="file" />""",
  ""])
@pytest.mark.parametrize("submit_file", [
    True,
    False
])
@pytest.mark.parametrize("enctype", [
  pytest.param("multipart/form-data"),
  pytest.param("application/x-www-form-urlencoded"),
  pytest.param("Invalid enctype")
])
def test_enctype_and_file_submit(httpbin, enctype, submit_file, file_field):
    # test if enctype is respected when specified
    # and if files are processed correctly
    form_html = """
    <form method="post" action="{}/post" enctype="{}">
      <input name="in" value="test" />
      {}
    </form>
    """.format(httpbin.url, enctype, file_field)
    form = BeautifulSoup(form_html, "lxml").form

    valid_enctype = (enctype in valid_enctypes_file_submit and
                     valid_enctypes_file_submit[enctype])
    expected_content = b""  # default
    if submit_file and file_field:
        # create a temporary file for testing file upload
        file_content = b":-)"
        pic_filedescriptor, pic_path = tempfile.mkstemp()
        os.write(pic_filedescriptor, file_content)
        os.close(pic_filedescriptor)
        if valid_enctype:
            # Correct encoding => send the content
            expected_content = file_content
        else:
            # Encoding doesn't allow sending the content, we expect
            # the filename as a normal text field.
            expected_content = pic_path.encode()
        form.find("input", {"name": "pic"})["value"] = pic_path

    browser = mechanicalsoup.Browser()
    response = browser._request(form)

    if enctype not in valid_enctypes_file_submit:
        expected_enctype = default_enctype
    else:
        expected_enctype = enctype
    assert expected_enctype in response.request.headers["Content-Type"]

    resp = response.json()
    assert resp["form"]["in"] == "test"

    found = False
    found_in = None

    for key, value in resp.items():
        if value:
            if "pic" in value:
                content = value["pic"].encode()
                assert not found
                assert key in ("files", "form")
                found = True
                found_in = key
            if key == "files" and not valid_enctype:
                assert not value

    assert found == bool(file_field)
    if file_field:
        assert content == expected_content

        if valid_enctype:
            assert found_in == "files"
            if submit_file:
                assert ("filename=\"" + pic_path + "\""
                        ).encode() in response.request.body
            else:
                assert b"filename=\"\"" in response.request.body
        else:
            assert found_in == "form"

    if submit_file and file_field:
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
    assert resp.status_code == 200 and resp.json()['form'] == data


if __name__ == '__main__':
    pytest.main(sys.argv)
