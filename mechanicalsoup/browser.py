import requests
import bs4
from six.moves import urllib
from six import string_types
from .form import Form


class Browser:

    def __init__(self, session=None, soup_config=None):
        self.session = session or requests.Session()
        self.soup_config = soup_config or dict()

    @staticmethod
    def add_soup(response, soup_config):
        if "text/html" in response.headers.get("Content-Type", ""):
            response.soup = bs4.BeautifulSoup(
                response.content, **soup_config)

    def request(self, *args, **kwargs):
        response = self.session.request(*args, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def post(self, *args, **kwargs):
        response = self.session.post(*args, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def _build_request(self, form, url=None, **kwargs):
        method = form["method"]
        action = form["action"]
        url = urllib.parse.urljoin(url, action)

        # read http://www.w3.org/TR/html5/forms.html
        data = kwargs.get("data") or dict()
        files = kwargs.get("files") or dict()

        for input in form.select("input"):
            name = input.get("name")
            # web browsers use empty string for inputs with missing values
            value = input.get("value", "")
            if not name:
                continue

            if input.get("type") in ("radio", "checkbox") \
                    and "checked" not in input.attrs:
                continue

            if input.get("type") == "checkbox":
                data.setdefault(name, []).append(value)

            elif input.get("type") == "file":
                # read http://www.cs.tut.fi/~jkorpela/forms/file.html
                # in web browsers, file upload only happens if the form"s (or
                # submit button"s) enctype attribute is set to
                # "multipart/form-data". we don"t care, simplify.
                if not value:
                    continue
                if isinstance(value, string_types):
                    value = open(value, "rb")
                files[name] = value

            else:
                data[name] = value

        for textarea in form.select("textarea"):
            name = textarea.get("name")
            if not name:
                continue
            data[name] = textarea.text

        for select in form.select("select"):
            name = select.get("name")
            if not name:
                continue
            for i, option in enumerate(select.select("option")):
                if i == 0 or "selected" in option.attrs:
                    data[name] = option.get("value", "")

        return requests.Request(method, url, data=data, files=files, **kwargs)

    def _prepare_request(self, form, url=None, **kwargs):
        request = self._build_request(form, url, **kwargs)
        return self.session.prepare_request(request)

    def submit(self, form, url=None, **kwargs):
        if isinstance(form, Form):
            form = form.form
        request = self._prepare_request(form, url, **kwargs)
        response = self.session.send(request)
        Browser.add_soup(response, self.soup_config)
        return response
