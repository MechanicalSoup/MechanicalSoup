import mechanicalsoup
import requests_mock
import pytest
try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = mechanicalsoup.Form(page.soup.form)

    input_data = {"custname": "Philip J. Fry"}
    form.input(input_data)

    check_data = {"size": "large", "topping": ["cheese"]}
    form.check(check_data)
    check_data = {"size": "medium", "topping": "onion"}
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


def test_submit_set():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = mechanicalsoup.Form(page.soup.form)

    form["custname"] = "Philip J. Fry"

    form["size"] = "medium"
    form["topping"] = ("cheese", "onion")

    form["comments"] = "freezer"

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


choose_submit_form = '''
<html>
  <body>
    <!-- vaguely based on Trac edit-page form -->
    <form id="choose-submit-form" method="post" action="mock://multi-button-form.com/post">
      <textarea id="text" class="wikitext trac-resizable" name="text" cols="80" rows="40">
      </textarea>
      <div class="field">
        <label>Comment about this change (optional):<br />
          <input id="comment" type="text" name="comment" size="80" value="" />
        </label>
      </div>
      <div class="buttons">
        <input type="submit" name="preview" value="Preview Page" /> 
        <input type="submit" name="diff" value="Review Changes" /> 
        <input type="submit" id="save" name="save" value="Submit changes" />
        <button type="submit" name="cancel" value="Cancel" />
      </div>
    </form>
  </body>
</html>
'''

def setup_mock_browser(expected_post=None):
    url = 'mock://multi-button-form.com'
    mock = requests_mock.Adapter()
    mock.register_uri('GET', url, headers={'Content-Type': 'text/html'}, text=choose_submit_form)
    if expected_post:
        def text_callback(request, context):
            query = parse_qsl(request.text)
            assert(set(query) == set(expected_post))
            return 'Success!'
        mock.register_uri('POST', url + '/post', text=text_callback)
    return mechanicalsoup.StatefulBrowser(requests_adapters={'mock': mock}), url

@pytest.mark.parametrize("expected_post", [
    pytest.param(
        [
            ('comment', 'Created new page'),
            ('save', 'Submit changes'),
            ('text', '= Heading =\n\nNew page here!\n')
        ], id='save'),
    pytest.param(
        [
            ('comment', 'Testing choosing cancel button'),
            ('cancel', 'Cancel'),
            ('text', '= Heading =\n\nNew page here!\n')
        ], id='cancel'),
])
def test_choose_submit(expected_post):
    browser, url = setup_mock_browser(expected_post=expected_post)
    browser.open(url)
    form = browser.select_form('#choose-submit-form')
    browser['text'] = expected_post[2][1]
    browser['comment'] = expected_post[0][1]
    found = form.choose_submit(expected_post[1][0])
    assert(found)
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')


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
    browser.open_fake_page(submit_form_noaction, url=url)
    form = browser.select_form('#choose-submit-form')
    browser['text1'] = 'newText1'
    res = browser.submit_selected()
    assert(res.status_code == 200 and browser.get_url() == url)

submit_form_action = '''
<html>
  <body>
    <form id="choose-submit-form" action="mock://multi-button-form.com">
      <input type="text" name="text1" value="someValue1" />
      <input type="text" name="text2" value="someValue2" />
      <input type="submit" name="save" />
    </form>
  </body>
</html>
'''

def test_form_action():
    browser, url = setup_mock_browser()
    browser.open_fake_page(submit_form_action, url="http://example.com/invalid/")
    form = browser.select_form('#choose-submit-form')
    browser['text1'] = 'newText1'
    res = browser.submit_selected()
    assert(res.status_code == 200 and browser.get_url() == url)
