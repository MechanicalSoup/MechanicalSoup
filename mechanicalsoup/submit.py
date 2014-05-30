import requests
import bs4
from six.moves import urllib

class Browser:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        return Page(response)

    def _build_request(self, form, url=None):
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

        return requests.Request(method, url, data=payload)

    def submit(self, form, url=None):
        request = self._build_request(form, url)
        request = self.session.prepare_request(request)
        response = self.session.send(request)
        return Page(response)

class Page:
    def __init__(self, response):
        self.response = response
        self.soup = bs4.BeautifulSoup(response.content)
