import mechanicalsoup
from bs4 import BeautifulSoup

def test_build_request():
    form_html = """
    <form method='post' action='/post'>
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
