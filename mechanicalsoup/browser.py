import requests
import bs4
from six.moves import urllib

class Browser:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    @staticmethod
    def add_soup(response):
        if 'text/html' in response.headers['Content-Type']:
            try:
                response.soup = bs4.BeautifulSoup(response.content)
            except:
                pass

    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        Browser.add_soup(response)
        return response

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
            if input.get('type') in ('radio', 'checkbox') and 'checked' not in input.attrs:
                continue
            value = input['value']
            if input.get('type') == 'checkbox':
                if not name in payload:
                    payload[name] = list()
                payload[name].append(value)
            else:
                payload[name] = value

        for textarea in form.select("textarea"):
            name = textarea.get('name')
            if not name:
                continue
            payload[name] = textarea.text

        return requests.Request(method, url, data=payload)

    def submit(self, form, url=None):
        request = self._build_request(form, url)
        request = self.session.prepare_request(request)
        response = self.session.send(request)
        Browser.add_soup(response)
        return response
