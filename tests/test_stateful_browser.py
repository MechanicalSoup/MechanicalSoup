import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import sys
import re
from bs4 import BeautifulSoup
from test_form import setup_mock_browser
import pytest
import webbrowser

def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent('testing https://github.com/hickford/MechanicalSoup')
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

    assert (json["headers"]["User-Agent"] ==
            'testing https://github.com/hickford/MechanicalSoup')
    # Ensure we haven't blown away any regular headers
    assert set(('Content-Length', 'Host', 'Content-Type', 'Connection', 'Accept',
            'User-Agent', 'Accept-Encoding')).issubset(json["headers"].keys())
    browser.close()


def test_no_404():
    browser = mechanicalsoup.StatefulBrowser()
    resp = browser.open("http://httpbin.org/nosuchpage")
    assert resp.status_code == 404
    browser.close()

def test_404():
    browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
    with pytest.raises(mechanicalsoup.LinkNotFoundError) as context:
        resp = browser.open("http://httpbin.org/nosuchpage")
    resp = browser.open("http://httpbin.org/")
    assert resp.status_code == 200
    browser.close()

def test_user_agent():
    browser = mechanicalsoup.StatefulBrowser(user_agent='007')
    resp = browser.open("http://httpbin.org/user-agent")
    assert resp.json() == {'user-agent': '007'}
    browser.close()

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
    browser.close()

def test_links():
    browser = mechanicalsoup.StatefulBrowser()
    html = '''<a class="bluelink" href="/blue" id="blue_link">A Blue Link</a>
              <a class="redlink" href="/red" id="red_link">A Red Link</a>'''
    expected = [BeautifulSoup(html).a]
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
    assert two_links == BeautifulSoup(html).find_all('a')
    browser.close()

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
    form = browser.select_form('#choose-submit-form')
    browser['text'] = expected_post[2][1]
    browser['comment'] = expected_post[0][1]
    res = browser.submit_selected(btnName = expected_post[1][0])
    assert(res.status_code == 200 and res.text == 'Success!')
    browser.close()

def test_get_set_debug():
    browser = mechanicalsoup.StatefulBrowser()
    # Debug mode is off by default
    assert(not browser.get_debug())
    browser.set_debug(True)
    assert(browser.get_debug())
    browser.close()

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
    browser.close()

def test_launch_browser(mocker):
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_debug(True)
    browser.open_fake_page('<html></html>')
    mocker.patch('webbrowser.open')
    with pytest.raises(mechanicalsoup.LinkNotFoundError) as context:
        browser.follow_link('nosuchlink')
    # mock.assert_called_once() not available on some versions :-(
    assert webbrowser.open.call_count == 1
    mocker.resetall()
    with pytest.raises(mechanicalsoup.LinkNotFoundError) as context:
        browser.select_form('nosuchlink')
    # mock.assert_called_once() not available on some versions :-(
    assert webbrowser.open.call_count == 1
    browser.close()

def test_find_link():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page('<html></html>')
    with pytest.raises(mechanicalsoup.LinkNotFoundError) as context:
        browser.find_link('nosuchlink')
    browser.close()

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
    browser.close()

if __name__ == '__main__':
    pytest.main(sys.argv)
