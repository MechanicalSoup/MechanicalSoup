import mechanicalsoup
from bs4 import BeautifulSoup

def test_build_request():
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
    """

    form = BeautifulSoup(form_html).form
    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)

    assert request.data['customer'] == 'Philip J. Fry' 
    assert request.data['telephone'] == '555' 
    assert request.data['comments'] == 'freezer' 
    assert request.data['size'] == 'medium' 
    assert request.data['topping'] == ['cheese', 'onion']

def test_submit_online():
    browser = mechanicalsoup.Browser()
    page = browser.get("http://httpbin.org/forms/post")
    form = page.soup.form

    form.find_next("input", {"name" : "custname"})['value'] = 'Philip J. Fry'
    form.find_next("input", {"name" : "custtel"})['value'] = '555'
    form.find_next("input", {"name" : "size", "value": "medium"})['checked'] = ""
    form.find_next("input", {"name" : "topping", "value": "cheese"})['checked'] = ""
    form.find_next("input", {"name" : "topping", "value": "onion"})['checked'] = ""
    # form.find_next("textarea", {"name" : "comments"}).text = 'freezer'

    response = browser.submit(form, page.url)
    json = response.json()
    data = json['form']
    assert data["custname"] == 'Philip J. Fry'
    assert data["custtel"] == '555'
    assert data["size"] == "medium"
    assert data["topping"] == ["cheese", "onion"]
    # assert data["comments"] == "freezer"

