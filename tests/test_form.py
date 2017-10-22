import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import sys
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
    browser.close()


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
    browser.close()


choose_submit_form = '''
<html>
  <body>
    <!-- vaguely based on Trac edit-page form -->
    <form id="choose-submit-form" method="post" action="mock://form.com/post">
      <textarea id="text" class="wikitext trac-resizable" name="text"
        cols="80" rows="40">
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


def setup_mock_browser(expected_post=None, text=choose_submit_form):
    url = 'mock://form.com'
    mock = requests_mock.Adapter()
    mock.register_uri('GET', url, headers={'Content-Type': 'text/html'},
                      text=text)
    if expected_post is not None:
        def text_callback(request, context):
            # Python 2's parse_qsl doesn't like None argument
            query = parse_qsl(request.text) if request.text else ()
            assert(set(query) == set(expected_post))
            return 'Success!'
        mock.register_uri('POST', url + '/post', text=text_callback)
    browser = mechanicalsoup.StatefulBrowser(requests_adapters={'mock': mock})
    return browser, url


@pytest.mark.parametrize("expected_post", [
    pytest.param(
        [
            ('comment', 'Testing preview page'),
            ('preview', 'Preview Page'),
            ('text', 'Setting some text!')
        ], id='preview'),
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
    form.choose_submit(expected_post[1][0])
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')
    browser.close()


choose_submit_fail_form = '''
<html>
  <form id="choose-submit-form">
    <input type="submit" name="test_submit" value="Test Submit" />
  </form>
</html>
'''


@pytest.mark.parametrize("select_name", [
    pytest.param({'name': 'does_not_exist', 'fails': True}, id='not found'),
    pytest.param({'name': 'test_submit', 'fails': False}, id='found'),
])
def test_choose_submit_fail(select_name):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page(choose_submit_fail_form)
    form = browser.select_form('#choose-submit-form')
    if select_name['fails']:
        with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
            form.choose_submit(select_name['name'])
    else:
        form.choose_submit(select_name['name'])
    browser.close()


choose_submit_multiple_match_form = '''
<html>
  <form id="choose-submit-form">
    <input type="submit" name="test_submit" value="First Submit" />
    <input type="submit" name="test_submit" value="Second Submit" />
  </form>
</html>
'''


def test_choose_submit_multiple_match():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page(choose_submit_multiple_match_form)
    form = browser.select_form('#choose-submit-form')
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.choose_submit('test_submit')
    browser.close()


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
    form['text1'] = 'newText1'
    res = browser.submit_selected()
    assert(res.status_code == 200 and browser.get_url() == url)
    browser.close()


submit_form_action = '''
<html>
  <body>
    <form id="choose-submit-form" action="mock://form.com">
      <input type="text" name="text1" value="someValue1" />
      <input type="text" name="text2" value="someValue2" />
      <input type="submit" name="save" />
    </form>
  </body>
</html>
'''


def test_form_action():
    browser, url = setup_mock_browser()
    # for info about example.com see: https://tools.ietf.org/html/rfc2606
    browser.open_fake_page(submit_form_action,
                           url="http://example.com/invalid/")
    form = browser.select_form('#choose-submit-form')
    form['text1'] = 'newText1'
    res = browser.submit_selected()
    assert(res.status_code == 200 and browser.get_url() == url)
    browser.close()


set_select_form = '''
<html>
  <form method="post" action="mock://form.com/post">
    <select name="entree">
      <option value="tofu" selected="selected">Tofu Stir Fry</option>
      <option value="curry">Red Curry</option>
      <option value="tempeh">Tempeh Tacos</option>
    </select>
    <input type="submit" value="Select" />
  </form>
</html>
'''


@pytest.mark.parametrize("option", [
    pytest.param({'result': [('entree', 'tofu')], 'default': True},
                 id='default'),
    pytest.param({'result': [('entree', 'curry')], 'default': False},
                 id='selected'),
])
def test_set_select(option):
    '''Test the branch of Form.set that finds "select" elements.'''
    browser, url = setup_mock_browser(expected_post=option['result'],
                                      text=set_select_form)
    browser.open(url)
    browser.select_form('form')
    if not option['default']:
        browser[option['result'][0][0]] = option['result'][0][1]
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')
    browser.close()


set_select_multiple_form = '''
<form method="post" action="mock://form.com/post">
  <select name="instrument" multiple>
    <option value="piano">Piano</option>
    <option value="bass">Bass</option>
    <option value="violin">Violin</option>
  </select>
  <input type="submit" value="Select Multiple" />
</form>
'''


@pytest.mark.parametrize("options", [
    pytest.param('bass', id='select one (str)'),
    pytest.param(('bass',), id='select one (tuple)'),
    pytest.param(('piano', 'violin'), id='select two'),
])
def test_set_select_multiple(options):
    """Test a <select multiple> element."""
    # When a browser submits multiple selections, the qsl looks like:
    #  name=option1&name=option2
    if not isinstance(options, list) and not isinstance(options, tuple):
        expected = (('instrument', options),)
    else:
        expected = (('instrument', option) for option in options)
    browser, url = setup_mock_browser(expected_post=expected,
                                      text=set_select_multiple_form)
    browser.open(url)
    form = browser.select_form('form')
    form.set_select({'instrument': options})
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')
    browser.close()


def test_form_not_found():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page(page_with_various_fields)
    form = browser.select_form('form')
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.input({'foo': 'bar', 'nosuchname': 'nosuchval'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.check({'foo': 'bar', 'nosuchname': 'nosuchval'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.check({'entree': 'cheese'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.check({'topping': 'tofu'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.textarea({'bar': 'value', 'foo': 'nosuchval'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.set_radio({'size': 'tiny'})
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.set_select({'entree': ('no_multiple', 'no_multiple')})
    browser.close()


page_with_radio = '''
<html>
  <form method="post">
    <input type=checkbox name="foo" value="bacon"> This is a checkbox
  </form>
</html>
'''


def test_form_check_uncheck():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page(page_with_radio, url="http://example.com/invalid/")
    form = browser.select_form('form')
    assert "checked" not in form.form.find("input", {"name": "foo"}).attrs

    form["foo"] = True
    assert form.form.find("input", {"name": "foo"}).attrs["checked"] == ""

    # Test explicit unchecking (skipping the call to Form.uncheck_all)
    form.set_checkbox({"foo": False}, uncheck_other_boxes=False)
    assert "checked" not in form.form.find("input", {"name": "foo"}).attrs
    browser.close()


page_with_various_fields = '''
<html>
  <form method="post">
    <input name="foo">
    <textarea name="bar">
    </textarea>
    <select name="entree">
      <option value="tofu" selected="selected">  Tofu Stir Fry </option>
      <option value="curry">    Red Curry</option>
      <option value="tempeh">Tempeh Tacos    </option>
    </select>
    <fieldset>
     <legend> Pizza Toppings </legend>
     <p><label> <input type=checkbox name="topping"
      value="bacon"> Bacon </label></p>
     <p><label> <input type=checkbox name="topping"
      value="cheese" checked>Extra Cheese   </label></p>
     <p><label> <input type=checkbox name="topping"
      value="onion" checked> Onion </label></p>
     <p><label> <input type=checkbox name="topping"
      value="mushroom"> Mushroom </label></p>
    </fieldset>
    <p><input name="size" type=radio value="small">Small</p>
    <p><input name="size" type=radio value="medium">Medium</p>
    <p><input name="size" type=radio value="large">Large</p>
    <input type="submit" value="Select" />
  </form>
</html>
'''


def test_form_print_summary(capsys):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open_fake_page(page_with_various_fields,
                           url="http://example.com/invalid/")
    browser.select_form("form")
    browser.get_current_form().print_summary()
    out, err = capsys.readouterr()
    # Different versions of bs4 show either <input></input> or
    # <input/>. Normalize before comparing.
    out = out.replace('></input>', '/>')
    assert out == """<input name="foo"/>
<textarea name="bar"></textarea>
<select name="entree">
<option selected="selected" value="tofu">Tofu Stir Fry</option>
<option value="curry">Red Curry</option>
<option value="tempeh">Tempeh Tacos</option>
</select>
<input name="topping" type="checkbox" value="bacon"/>
<input checked="" name="topping" type="checkbox" value="cheese"/>
<input checked="" name="topping" type="checkbox" value="onion"/>
<input name="topping" type="checkbox" value="mushroom"/>
<input name="size" type="radio" value="small"/>
<input name="size" type="radio" value="medium"/>
<input name="size" type="radio" value="large"/>
<input type="submit" value="Select"/>
"""
    assert err == ""


if __name__ == '__main__':
    pytest.main(sys.argv)
