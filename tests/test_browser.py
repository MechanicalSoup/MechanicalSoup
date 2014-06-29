import mechanicalsoup
from bs4 import BeautifulSoup
import tempfile

def test_submit_online():
    """Complete and submit the pizza form at http://httpbin.org/forms/post """
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = page.soup.form

    form.find("input", {"name" : "custname"})['value'] = 'Philip J. Fry'
    assert 'value' not in form.find('input', {'name' : 'custtel'}).attrs # leave custtel blank without value
    form.find("input", {"name" : "size", "value": "medium"})['checked'] = ""
    form.find("input", {"name" : "topping", "value": "cheese"})['checked'] = ""
    form.find("input", {"name" : "topping", "value": "onion"})['checked'] = ""
    form.find("textarea", {"name" : "comments"}).insert(0, 'freezer')

    response = browser.submit(form, page.url)

    # helpfully the form submits to http://httpbin.org/post which simply returns the request headers in json format
    json = response.json()
    data = json['form']
    assert data["custname"] == 'Philip J. Fry'
    assert data["custtel"] == '' # web browser submits '' for input left blank
    assert data["size"] == "medium"
    assert data["topping"] == ["cheese", "onion"]
    assert data["comments"] == "freezer"

form_html = """
<form method='post' action='http://httpbin.org/post'>
<input name='customer' value='Philip J. Fry'/>
<input name='telephone' value='555'/>
<textarea name='comments'>freezer</textarea> 
<fieldset>
 <legend> Pizza Size </legend>
 <p><label> <input type=radio name=size value="small"> Small </label></p>
 <p><label> <input type=radio name=size value="medium" checked> Medium </label></p>
 <p><label> <input type=radio name=size value="large"> Large </label></p>
</fieldset>
<fieldset>
 <legend> Pizza Toppings </legend>
 <p><label> <input type=checkbox name="topping" value="bacon"> Bacon </label></p>
 <p><label> <input type=checkbox name="topping" value="cheese" checked> Extra Cheese </label></p>
 <p><label> <input type=checkbox name="topping" value="onion" checked> Onion </label></p>
 <p><label> <input type=checkbox name="topping" value="mushroom"> Mushroom </label></p>
</fieldset>
<input name="pic" type="file">
"""

def test_build_request():
    form = BeautifulSoup(form_html).form

    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)

    assert request.data['customer'] == 'Philip J. Fry' 
    assert request.data['telephone'] == '555' 
    assert request.data['comments'] == 'freezer' 
    assert request.data['size'] == 'medium' 
    assert request.data['topping'] == ['cheese', 'onion']

    request = browser._prepare_request(form)
    assert "application/x-www-form-urlencoded" in request.headers['Content-Type']

def test_prepare_request_file():
    form = BeautifulSoup(form_html).form

    # create a temporary file for testing file upload
    pic_path = tempfile.mkstemp()[1]
    with open(pic_path, 'w') as f:
        f.write(":-)")

    form.find("input", {"name" : "pic" })['value'] = pic_path

    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)

    assert request.files
    assert request.files["pic"]
    assert request.files["pic"].read() == ":-)".encode("utf8")
    assert "pic" not in request.data

    request = browser._prepare_request(form)
    assert "multipart/form-data" in request.headers['Content-Type']
    