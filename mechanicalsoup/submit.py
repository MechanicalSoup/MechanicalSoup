import requests
import bs4
import urllib.parse

class Browser:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        return Page(response)

    def submit(self, form, url=None):
        method = form['method']
        action = form['action']
        url = urllib.parse.urljoin(url, action)

        # read http://www.w3.org/TR/html5/forms.html
        payload = dict()
        for input in form.select("input"):
            name = input.get('name')
            if not name:
                continue
            value = input['value']
            payload[name] = value

        for textarea in form.select("textarea"):
            name = input.get('name')
            if not name:
                continue
            payload[name] = textarea.text

        return Page(self.session.post(url, data=payload))

class Page:
    def __init__(self, response):
        self.response = response
        self.soup = bs4.BeautifulSoup(response.content)
