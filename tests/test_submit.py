import mechanicalsoup
from bs4 import BeautifulSoup

def test_build_request():
    form_html = """
    <form method='post' action='/post'>
    <input name='custname' value='I.C. Weiner'>
    """
    form = BeautifulSoup(form_html).form
    browser = mechanicalsoup.Browser()
    request = browser._build_request(form)
    assert request.data['custname'] == 'I.C. Weiner' 
