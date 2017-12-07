import tempfile
import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import sys
import re
from bs4 import BeautifulSoup
from utils import setup_mock_browser
import pytest
import webbrowser


def test_request_forward():
    browser, url = setup_mock_browser(expected_post=[('var1', 'val1'),
                                                     ('var2', 'val2')])
    r = browser.request('POST', url + '/post', data={'var1': 'val1',
                                                     'var2': 'val2'})
    assert r.text == 'Success!'


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent('testing MechanicalSoup')
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
    browser["topping"] = ("cheese", "bacon")
    # Change our mind to make sure old boxes are unticked
    browser["topping"] = ("cheese", "onion")
    browser["comments"] = "Some comment here"
    browser.get_current_form().set("nosuchfield", "new value", True)
    response = browser.submit_selected()
    json = response.json()
    data = json["form"]
    assert data["custname"] == "Customer Name Here"
    assert data["custtel"] == ""  # web browser submits "" for input left blank
    assert data["size"] == "medium"
    assert set(data["topping"]) == set(("cheese", "onion"))
    assert data["comments"] == "Some comment here"
    assert data["nosuchfield"] == "new value"

    assert json["headers"]["User-Agent"] == 'testing MechanicalSoup'
    # Ensure we haven't blown away any regular headers
    expected_headers = ('Content-Length', 'Host', 'Content-Type', 'Connection',
                        'Accept', 'User-Agent', 'Accept-Encoding')
    assert set(expected_headers).issubset(json["headers"].keys())


def test_no_404():
    browser = mechanicalsoup.StatefulBrowser()
    resp = browser.open("http://httpbin.org/nosuchpage")
    assert resp.status_code == 404


def test_404():
    browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        resp = browser.open("http://httpbin.org/nosuchpage")
    resp = browser.open("http://httpbin.org/")
    assert resp.status_code == 200


def test_user_agent():
    browser = mechanicalsoup.StatefulBrowser(user_agent='007')
    resp = browser.open("http://httpbin.org/user-agent")
    assert resp.json() == {'user-agent': '007'}


def test_open_relative():
    # Open an arbitrary httpbin page to set the current URL
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://httpbin.org/html")

    # Open a relative page and make sure remote host and browser agree on URL
    resp = browser.open_relative("/get")
    assert resp.json()['url'] == "http://httpbin.org/get"
    assert browser.get_url() == "http://httpbin.org/get"

    # Test passing additional kwargs to the session
    resp = browser.open_relative("/basic-auth/me/123", auth=('me', '123'))
    assert browser.get_url() == "http://httpbin.org/basic-auth/me/123"
    assert resp.json() == {"authenticated": True, "user": "me"}


def test_links():
    browser = mechanicalsoup.StatefulBrowser()
    html = '''<a class="bluelink" href="/blue" id="blue_link">A Blue Link</a>
              <a class="redlink" href="/red" id="red_link">A Red Link</a>'''
    expected = [BeautifulSoup(html, "lxml").a]
    browser.open_fake_page(html)

    # Test StatefulBrowser.links url_regex argument
    assert browser.links(url_regex="bl") == expected
    assert browser.links(url_regex="bluish") == []

    # Test StatefulBrowser.links link_text argument
    assert browser.links(link_text="A Blue Link") == expected
    assert browser.links(link_text="Blue") == []

    # Test StatefulBrowser.links kwargs passed to BeautifulSoup.find_all
    assert browser.links(string=re.compile('Blue')) == expected
    assert browser.links(class_="bluelink") == expected
    assert browser.links(id="blue_link") == expected
    assert browser.links(id="blue") == []

    # Test returning a non-singleton
    two_links = browser.links(id=re.compile('_link'))
    assert len(two_links) == 2
    assert two_links == BeautifulSoup(html, "lxml").find_all('a')


@pytest.mark.parametrize("expected_post", [
    pytest.param(
        [
            ('comment', 'Selecting an input submit'),
            ('diff', 'Review Changes'),
            ('text', 'Setting some text!')
        ], id='input'),
    pytest.param(
        [
            ('comment', 'Selecting a button submit'),
            ('cancel', 'Cancel'),
            ('text', '= Heading =\n\nNew page here!\n')
        ], id='button'),
])
def test_submit_btnName(expected_post):
    '''Tests that the btnName argument chooses the submit button.'''
    browser, url = setup_mock_browser(expected_post=expected_post)
    browser.open(url)
    browser.select_form('#choose-submit-form')
    browser['text'] = expected_post[2][1]
    browser['comment'] = expected_post[0][1]
    res = browser.submit_selected(btnName=expected_post[1][0])
    assert(res.status_code == 200 and res.text == 'Success!')


def test_get_set_debug():
    browser = mechanicalsoup.StatefulBrowser()
    # Debug mode is off by default
    assert(not browser.get_debug())
    browser.set_debug(True)
    assert(browser.get_debug())


def test_list_links(capsys):
    # capsys is a pytest fixture that allows us to inspect the std{err,out}
    browser = mechanicalsoup.StatefulBrowser()
    links = '''
     <a href="/link1">Link #1</a>
     <a href="/link2" id="link2"> Link #2</a>
'''
    browser.open_fake_page('<html>{0}</html>'.format(links))
    browser.list_links()
    out, err = capsys.readouterr()
    expected = 'Links in the current page:{0}'.format(links)
    assert out == expected


def test_launch_browser(mocker):
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_debug(True)
    browser.open_fake_page('<html></html>')
    mocker.patch('webbrowser.open')
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        browser.follow_link('nosuchlink')
    # mock.assert_called_once() not available on some versions :-(
    assert webbrowser.open.call_count == 1
    mocker.resetall()
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        browser.select_form('nosuchlink')
    # mock.assert_called_once() not available on some versions :-(
    assert webbrowser.open.call_count == 1


def test_find_link():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page('<html></html>')
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        browser.find_link('nosuchlink')


def test_verbose(capsys):
    '''Tests that the btnName argument chooses the submit button.'''
    browser, url = setup_mock_browser()
    browser.open(url)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    assert browser.get_verbose() == 0
    browser.set_verbose(1)
    browser.open(url)
    out, err = capsys.readouterr()
    assert out == "."
    assert err == ""
    assert browser.get_verbose() == 1
    browser.set_verbose(2)
    browser.open(url)
    out, err = capsys.readouterr()
    assert out == "mock://form.com\n"
    assert err == ""
    assert browser.get_verbose() == 2


def test_new_control():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://httpbin.org/forms/post")
    browser.select_form("form")
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        # The control doesn't exist, yet.
        browser["temperature"] = "cold"
    browser["size"] = "large"  # Existing radio
    browser["comments"] = "This is a comment"  # Existing textarea
    browser.new_control("text", "temperature", "warm")
    browser.new_control("textarea", "size", "Sooo big !")
    browser.new_control("text", "comments", "This is an override comment")
    browser.new_control("checkbox", "foo", "valval", checked="checked")
    tag = browser.get_current_form().form.find("input", {"name": "foo"})
    assert tag.attrs["checked"] == "checked"
    browser["temperature"] = "hot"
    response = browser.submit_selected()
    json = response.json()
    data = json["form"]
    print(data)
    assert data["temperature"] == "hot"
    assert data["size"] == "Sooo big !"
    assert data["comments"] == "This is an override comment"
    assert data["foo"] == "valval"


submit_form_noaction = '''
<html>
  <body>
    <form id="choose-submit-form">
      <input type="text" name="text1" value="someValue1" />
      <input type="text" name="text2" value="someValue2" />
      <input type="submit" name="save" />
    </form>
  </body>
</html>
'''


def test_form_noaction():
    browser, url = setup_mock_browser()
    browser.open_fake_page(submit_form_noaction)
    browser.select_form('#choose-submit-form')
    with pytest.raises(ValueError, message="no URL to submit to"):
        browser.submit_selected()


submit_form_noname = '''
<html>
  <body>
    <form id="choose-submit-form" method="post" action="mock://form.com/post">
      <textarea>Value</textarea> <!-- no name -->
      <select> <!-- no name -->
        <option value="tofu" selected="selected">Tofu Stir Fry</option>
        <option value="curry">Red Curry</option>
        <option value="tempeh">Tempeh Tacos</option>
      </select>
    </form>
  </body>
</html>
'''


def test_form_noname():
    browser, url = setup_mock_browser(expected_post=[])
    browser.open_fake_page(submit_form_noname, url=url)
    browser.select_form('#choose-submit-form')
    response = browser.submit_selected()
    assert(response.status_code == 200 and response.text == 'Success!')


submit_form_multiple = '''
<html>
  <body>
    <form id="choose-submit-form" method="post" action="mock://form.com/post">
      <select name="foo" multiple>
        <option value="tofu" selected="selected">Tofu Stir Fry</option>
        <option value="curry">Red Curry</option>
        <option value="tempeh" selected="selected">Tempeh Tacos</option>
      </select>
    </form>
  </body>
</html>
'''


def test_form_multiple():
    browser, url = setup_mock_browser(expected_post=[('foo', 'tempeh'),
                                                     ('foo', 'tofu')])
    browser.open_fake_page(submit_form_multiple, url=url)
    browser.select_form('#choose-submit-form')
    response = browser.submit_selected()
    assert(response.status_code == 200 and response.text == 'Success!')


def test_upload_file():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://httpbin.org/forms/post")

    # Create two temporary files to upload
    def make_file(content):
        path = tempfile.mkstemp()[1]
        with open(path, "w") as f:
            f.write(content)
        return path
    path1, path2 = (make_file(content) for content in
                    ("first file content", "second file content"))

    # The form doesn't have a type=file field, but the target action
    # does show it => add the fields ourselves.
    browser.select_form()
    browser.new_control("file", "first", path1)
    browser.new_control("file", "second", "")
    browser["second"] = path2
    browser.get_current_form().print_summary()
    response = browser.submit_selected()
    files = response.json()["files"]
    assert files["first"] == "first file content"
    assert files["second"] == "second file content"


def test_with():
    """Test that __enter__/__exit__ properly create/close the browser."""
    with mechanicalsoup.StatefulBrowser() as browser:
        assert browser.session is not None
    assert browser.session is None


def test_select_form_nr():
    """Test the nr option of select_form."""
    forms = """<form id="a"></form><form id="b"></form><form id="c"></form>"""
    with mechanicalsoup.StatefulBrowser() as browser:
        browser.open_fake_page(forms)
        form = browser.select_form()
        assert form.form['id'] == "a"
        form = browser.select_form(nr=1)
        assert form.form['id'] == "b"
        form = browser.select_form(nr=2)
        assert form.form['id'] == "c"
        with pytest.raises(mechanicalsoup.LinkNotFoundError):
            browser.select_form(nr=3)


if __name__ == '__main__':
    pytest.main(sys.argv)
