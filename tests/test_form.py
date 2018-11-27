import setpath  # noqa:F401, must come before 'import mechanicalsoup'
import mechanicalsoup
import bs4
from utils import setup_mock_browser
import sys
import pytest


def test_construct_form_fail():
    """Form objects must be constructed from form html elements."""
    soup = bs4.BeautifulSoup('<notform>This is not a form</notform>', 'lxml')
    tag = soup.find('notform')
    assert isinstance(tag, bs4.element.Tag)
    pytest.deprecated_call(mechanicalsoup.Form, tag)


def test_submit_online(httpbin):
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get(httpbin + "/forms/post")
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


def test_submit_set(httpbin):
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get(httpbin + "/forms/post")
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


@pytest.mark.parametrize("value", [
    pytest.param('continue', id='first'),
    pytest.param('cancel', id='second'),
])
def test_choose_submit_from_selector(value):
    """Test choose_submit by passing a CSS selector argument."""
    text = """
    <form method="post" action="mock://form.com/post">
      <input type="submit" name="do" value="continue" />
      <input type="submit" name="do" value="cancel" />
    </form>"""
    browser, url = setup_mock_browser(expected_post=[('do', value)], text=text)
    browser.open(url)
    form = browser.select_form()
    submits = form.form.select('input[value="{}"]'.format(value))
    assert len(submits) == 1
    form.choose_submit(submits[0])
    res = browser.submit_selected()
    assert res.status_code == 200 and res.text == 'Success!'


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


def test_choose_submit_twice():
    """Test that calling choose_submit twice fails."""
    text = '''
    <form>
      <input type="submit" name="test1" value="Test1" />
      <input type="submit" name="test2" value="Test2" />
    </form>
    '''
    soup = bs4.BeautifulSoup(text, 'lxml')
    form = mechanicalsoup.Form(soup.form)
    form.choose_submit('test1')
    expected_msg = 'Submit already chosen. Cannot change submit!'
    with pytest.raises(Exception, match=expected_msg):
        form.choose_submit('test2')


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
        expected = [('instrument', options)]
    else:
        expected = [('instrument', option) for option in options]
    browser, url = setup_mock_browser(expected_post=expected,
                                      text=set_select_multiple_form)
    browser.open(url)
    form = browser.select_form('form')
    form.set_select({'instrument': options})
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')


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
    <button name="action"  value="cancel">Cancel</button>
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
<button name="action" value="cancel">Cancel</button>
<input type="submit" value="Select"/>
"""
    assert err == ""


def test_issue180():
    """Test that a KeyError is not raised when Form.choose_submit is called
    on a form where a submit element is missing its name-attribute."""
    browser = mechanicalsoup.StatefulBrowser()
    html = '''
<form>
  <input type="submit" value="Invalid" />
  <input type="submit" name="valid" value="Valid" />
</form>
'''
    browser.open_fake_page(html)
    form = browser.select_form()
    with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
        form.choose_submit('not_found')


def test_issue158():
    """Test that form elements are processed in their order on the page
    and that elements with duplicate name-attributes are not clobbered."""
    issue158_form = '''
<form method="post" action="mock://form.com/post">
  <input name="box" type="hidden" value="1"/>
  <input checked="checked" name="box" type="checkbox" value="2"/>
  <input name="box" type="hidden" value="0"/>
  <input type="submit" value="Submit" />
</form>
'''
    expected_post = [('box', '1'), ('box', '2'), ('box', '0')]
    browser, url = setup_mock_browser(expected_post=expected_post,
                                      text=issue158_form)
    browser.open(url)
    browser.select_form()
    res = browser.submit_selected()
    assert(res.status_code == 200 and res.text == 'Success!')
    browser.close()


@pytest.mark.parametrize("expected_post", [
    pytest.param([('sub2', 'val2')], id='submit button'),
    pytest.param([('sub4', 'val4')], id='typeless button'),
    pytest.param([('sub5', 'val5')], id='submit input'),
])
def test_choose_submit_buttons(expected_post):
    """Buttons of type reset and button are not valid submits"""
    text = """
    <form method="post" action="mock://form.com/post">
      <button type="button" name="sub1" value="val1">Val1</button>
      <button type="submit" name="sub2" value="val2">Val2</button>
      <button type="reset" name="sub3" value="val3">Val3</button>
      <button name="sub4" value="val4">Val4</button>
      <input type="submit" name="sub5" value="val5">
    </form>
    """
    browser, url = setup_mock_browser(expected_post=expected_post, text=text)
    browser.open(url)
    browser.select_form()
    res = browser.submit_selected(btnName=expected_post[0][0])
    assert res.status_code == 200 and res.text == 'Success!'


@pytest.mark.parametrize("fail, selected, expected_post", [
    pytest.param(False, 'with_value', [('selector', 'with_value')],
                 id='Option with value'),
    pytest.param(False, 'Without value', [('selector', 'Without value')],
                 id='Option without value'),
    pytest.param(False, 'We have a value here', [('selector', 'with_value')],
                 id='Option with value selected by its text'),
    pytest.param(True, 'Unknown option', None,
                 id='Unknown option, must raise a LinkNotFound exception')
])
def test_option_without_value(fail, selected, expected_post):
    """Option tag in select can have no value option"""
    text = """
    <form method="post" action="mock://form.com/post">
      <select name="selector">
        <option value="with_value">We have a value here</option>
        <option>Without value</option>
      </select>
      <button type="submit">Submit</button>
    </form>
    """
    browser, url = setup_mock_browser(expected_post=expected_post,
                                      text=text)
    browser.open(url)
    browser.select_form()
    if fail:
        with pytest.raises(mechanicalsoup.utils.LinkNotFoundError):
            browser['selector'] = selected
    else:
        browser['selector'] = selected

        res = browser.submit_selected()
        assert res.status_code == 200 and res.text == 'Success!'


if __name__ == '__main__':
    pytest.main(sys.argv)
