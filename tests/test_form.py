import mechanicalsoup
import requests_mock, urllib


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
        <input type="submit" name="cancel" value="Cancel" />
      </div>
    </form>
  </body>
</html>
'''

def test_choose_submit():
    url = 'mock://multi-button-form.com'
    mock = requests_mock.Adapter()
    mock.register_uri('GET', url, headers={'Content-Type': 'text/html'}, text=choose_submit_form)
    def text_callback(request, context):
        expect = [('comment', 'Created new page'),
                ('save', 'Submit changes'),
                ('text', '= Heading =\n\nNew page here!\n')]
        query = urllib.parse.parse_qsl(request.text)
        assert(set(query) == set(expect))
        return 'Success!'
    mock.register_uri('POST', url + '/post', text=text_callback)

    browser = mechanicalsoup.StatefulBrowser(requests_adapters={'mock': mock})
    browser.open(url)
    form = browser.select_form('#choose-submit-form')
    browser['text'] = '= Heading =\n\nNew page here!\n'
    browser['comment'] = 'Created new page'
    found = form.choose_submit('save')
    assert(found)
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')


if __name__ == '__main__':
    test_submit_online()
    test_submit_set()
    test_choose_submit()
