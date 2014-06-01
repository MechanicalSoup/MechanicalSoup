import mechanicalsoup
from bs4 import BeautifulSoup

def test_build_request():
    form_html = """
    <form method='post' action='/post'>
    <input name='customer' value='Philip J. Fry'/>
    <textarea name='comments'>freezer</textarea> 
    """
    form = BeautifulSoup(form_html).form
    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)
    assert request.data['customer'] == 'Philip J. Fry' 
    assert request.data['comments'] == 'freezer' 
