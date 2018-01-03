import requests
import bs4
from six.moves import urllib
from six import string_types
from .form import Form
import webbrowser
import tempfile
from .utils import LinkNotFoundError
from .__version__ import __version__, __title__
import weakref


class Browser(object):
    """Builds a Browser.

    :param session: Attach a pre-existing requests Session instead of
        constructing a new one.
    :param soup_config: Configuration passed to BeautifulSoup to affect
        the way HTML is parsed. Defaults to ``{'features': 'lxml'}``.
        If overriden, it is highly recommended to `specify a parser
        <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use>`__.
        Otherwise, BeautifulSoup will issue a warning and pick one for
        you, but the parser it chooses may be different on different
        machines.
    :param requests_adapters: Configuration passed to requests, to affect
        the way HTTP requests are performed.
    :param raise_on_404: If True, raise :class:`LinkNotFoundError`
        when visiting a page triggers a 404 Not Found error.
    :param user_agent: Set the user agent header to this value.

    See also: :func:`StatefulBrowser`

    """
    def __init__(self, session=None, soup_config={'features': 'lxml'},
                 requests_adapters=None,
                 raise_on_404=False, user_agent=None):

        self.raise_on_404 = raise_on_404
        self.session = session or requests.Session()

        if hasattr(weakref, 'finalize'):
            self._finalize = weakref.finalize(self.session, self.close)
        else:   # pragma: no cover
            # Python < 3 does not have weakref.finalize, but these
            # versions accept calling session.close() within __del__
            self._finalize = self.close

        self.set_user_agent(user_agent)

        if requests_adapters is not None:
            for adaptee, adapter in requests_adapters.items():
                self.session.mount(adaptee, adapter)

        self.soup_config = soup_config or dict()

    @staticmethod
    def add_soup(response, soup_config):
        """Attaches a soup object to a requests response."""
        if "text/html" in response.headers.get("Content-Type", ""):
            response.soup = bs4.BeautifulSoup(response.content, **soup_config)
        else:
            response.soup = None

    def set_cookiejar(self, cookiejar):
        """Replaces the current cookiejar in the requests session. Since the
        session handles cookies automatically without calling this function,
        only use this when default cookie handling is insufficient.

        :param cookiejar: Any `cookielib.CookieJar
          <https://docs.python.org/2/library/cookielib.html#cookielib.CookieJar>`__
          compatible object.
        """
        self.session.cookies = cookiejar

    def get_cookiejar(self):
        """Gets the cookiejar from the requests session."""
        return self.session.cookies

    def set_user_agent(self, user_agent):
        """Replaces the current user agent in the requests session headers."""
        # set a default user_agent if not specified
        if user_agent is None:
            requests_ua = requests.utils.default_user_agent()
            user_agent = '%s (%s/%s)' % (requests_ua, __title__, __version__)

        # the requests module uses a case-insensitive dict for session headers
        self.session.headers['User-agent'] = user_agent

    def request(self, *args, **kwargs):
        """Straightforward wrapper around `requests.Session.request
        <http://docs.python-requests.org/en/master/api/#requests.Session.request>`__.

        :return: `requests.Response
            <http://docs.python-requests.org/en/master/api/#requests.Response>`__
            object with a *soup*-attribute added by :func:`add_soup`.

        This is a low-level function that should not be called for
        basic usage (use :func:`get` or :func:`post` instead). Use it if you
        need an HTTP verb that MechanicalSoup doesn't manage (e.g. MKCOL) for
        example.
        """
        response = self.session.request(*args, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def get(self, *args, **kwargs):
        """Straightforward wrapper around `requests.Session.get
        <http://docs.python-requests.org/en/master/api/#requests.Session.get>`__.

        :return: `requests.Response
            <http://docs.python-requests.org/en/master/api/#requests.Response>`__
            object with a *soup*-attribute added by :func:`add_soup`.
        """
        response = self.session.get(*args, **kwargs)
        if self.raise_on_404 and response.status_code == 404:
            raise LinkNotFoundError()
        Browser.add_soup(response, self.soup_config)
        return response

    def post(self, *args, **kwargs):
        """Straightforward wrapper around `requests.Session.post
        <http://docs.python-requests.org/en/master/api/#requests.Session.post>`__.

        :return: `requests.Response
            <http://docs.python-requests.org/en/master/api/#requests.Response>`__
            object with a *soup*-attribute added by :func:`add_soup`.
        """
        response = self.session.post(*args, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def _request(self, form, url=None, **kwargs):
        method = str(form.get("method", "get"))
        action = form.get("action")
        url = urllib.parse.urljoin(url, action)
        if url is None:  # This happens when both `action` and `url` are None.
            raise ValueError('no URL to submit to')

        # read http://www.w3.org/TR/html5/forms.html
        data = kwargs.pop("data", dict())
        files = kwargs.pop("files", dict())

        for input in form.select("input[name], button[name]"):
            name = input.get("name")

            if input.get("type") in ("radio", "checkbox"):
                if "checked" not in input.attrs:
                    continue
                value = input.get("value", "on")
            else:
                # web browsers use empty string for inputs with missing values
                value = input.get("value", "")

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
            multiple = "multiple" in select.attrs
            values = []
            for i, option in enumerate(select.select("option")):
                if (i == 0 and not multiple) or "selected" in option.attrs:
                    values.append(option.get("value", ""))
            if multiple:
                data[name] = values
            elif values:
                data[name] = values[-1]

        if method.lower() == "get":
            kwargs["params"] = data
        else:
            kwargs["data"] = data

        return self.session.request(method, url, files=files, **kwargs)

    def submit(self, form, url=None, **kwargs):
        """Prepares and sends a form request.

        :param form: The filled-out form.
        :param url: URL of the page the form is on. If the form action is a
            relative path, then this must be specified.
        :param \*\*kwargs: Arguments forwarded to `requests.Session.request
            <http://docs.python-requests.org/en/master/api/#requests.Session.request>`__.

        :return: `requests.Response
            <http://docs.python-requests.org/en/master/api/#requests.Response>`__
            object with a *soup*-attribute added by :func:`add_soup`.
        """
        if isinstance(form, Form):
            form = form.form
        response = self._request(form, url, **kwargs)
        Browser.add_soup(response, self.soup_config)
        return response

    def launch_browser(self, soup):
        """Launch a browser to display a page, for debugging purposes.

        :param: soup: Page contents to display, supplied as a bs4 soup object.
        """
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(soup.encode())
        webbrowser.open('file://' + file.name)

    def close(self):
        """Close the current session, if still open."""
        if self.session is not None:
            self.session.cookies.clear()
            self.session.close()
            self.session = None

    def __del__(self):
        self._finalize()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
