from __future__ import print_function

from six.moves import urllib
from .browser import Browser
from .utils import LinkNotFoundError
from .form import Form
import sys
import re
import bs4


class _BrowserState:
    def __init__(self, page=None, url=None, form=None, request=None):
        self.page = page
        self.url = url
        self.form = form
        self.request = request


class StatefulBrowser(Browser):
    """An extension of :class:`Browser` that stores the browser's state
    and provides many convenient functions for interacting with HTML elements.
    It is the primary tool in MechanicalSoup for interfacing with websites.

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

    All arguments are forwarded to :func:`Browser`.

    Examples ::

        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},  # Use the lxml HTML parser
            raise_on_404=True,
            user_agent='MyBot/0.1: mysite.example.com/bot_info',
        )
        browser.open(url)
        # ...
        browser.close()

    Once not used anymore, the browser can be closed
    using :func:`~Browser.close`.
    """

    def __init__(self, *args, **kwargs):
        super(StatefulBrowser, self).__init__(*args, **kwargs)
        self.__debug = False
        self.__verbose = 0
        self.__state = _BrowserState()

    def set_debug(self, debug):
        """Set the debug mode (off by default).

        Set to True to enable debug mode. When active, some actions
        will launch a browser on the current page on failure to let
        you inspect the page content.
        """
        self.__debug = debug

    def get_debug(self):
        """Get the debug mode (off by default)."""
        return self.__debug

    def set_verbose(self, verbose):
        """Set the verbosity level (an integer).

        * 0 means no verbose output.
        * 1 shows one dot per visited page (looks like a progress bar)
        * >= 1 shows each visited URL.
        """
        self.__verbose = verbose

    def get_verbose(self):
        """Get the verbosity level. See :func:`set_verbose()`."""
        return self.__verbose

    def get_url(self):
        """Get the URL of the currently visited page."""
        return self.__state.url

    def get_current_form(self):
        """Get the currently selected form as a :class:`Form` object.
        See :func:`select_form`.
        """
        return self.__state.form

    def __setitem__(self, name, value):
        """Call item assignment on the currently selected form.
        See :func:`Form.__setitem__`.
        """
        self.get_current_form()[name] = value

    def new_control(self, type, name, value, **kwargs):
        """Call :func:`Form.new_control` on the currently selected form."""
        return self.get_current_form().new_control(type, name, value, **kwargs)

    def get_current_page(self):
        """Get the current page as a soup object."""
        return self.__state.page

    def absolute_url(self, url):
        """Return the absolute URL made from the current URL and ``url``.
        The current URL is only used to provide any missing components of
        ``url``, as in the `.urljoin() method of urllib.parse
        <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin>`__.
        """
        return urllib.parse.urljoin(self.get_url(), url)

    def open(self, url, *args, **kwargs):
        """Open the URL and store the Browser's state in this object.
        All arguments are forwarded to :func:`Browser.get`.

        :return: Forwarded from :func:`Browser.get`.
        """
        if self.__verbose == 1:
            sys.stdout.write('.')
            sys.stdout.flush()
        elif self.__verbose >= 2:
            print(url)

        resp = self.get(url, *args, **kwargs)
        self.__state = _BrowserState(page=resp.soup, url=resp.url,
                                     request=resp.request)
        return resp

    def open_fake_page(self, page_text, url=None, soup_config=None):
        """Mock version of :func:`open`.

        Behave as if opening a page whose text is ``page_text``, but do not
        perform any network access. If ``url`` is set, pretend it is the page's
        URL. Useful mainly for testing.
        """
        soup_config = soup_config or self.soup_config
        self.__state = _BrowserState(
            page=bs4.BeautifulSoup(page_text, **soup_config),
            url=url)

    def open_relative(self, url, *args, **kwargs):
        """Like :func:`open`, but ``url`` can be relative to the currently
        visited page.
        """
        return self.open(self.absolute_url(url), *args, **kwargs)

    def refresh(self):
        """Reload the current page with the same request as originally done.
        Any change (`select_form`, or any value filled-in in the form) made to
        the current page before refresh is discarded.

        :raise ValueError: Raised if no refreshable page is loaded, e.g., when
            using the shallow ``Browser`` wrapper functions.

        :return: Response of the request."""
        old_request = self.__state.request
        if old_request is None:
            raise ValueError('The current page is not refreshable. Either no '
                             'page is opened or low-level browser methods '
                             'were used to do so')

        resp = self.session.send(old_request)
        Browser.add_soup(resp, self.soup_config)
        self.__state = _BrowserState(page=resp.soup, url=resp.url,
                                     request=resp.request)
        return resp

    def select_form(self, selector="form", nr=0):
        """Select a form in the current page.

        :param selector: CSS selector or a bs4.element.Tag object to identify
            the form to select.
            If not specified, ``selector`` defaults to "form", which is
            useful if, e.g., there is only one form on the page.
            For ``selector`` syntax, see the `.select() method in BeautifulSoup
            <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors>`__.
        :param nr: A zero-based index specifying which form among those that
            match ``selector`` will be selected. Useful when one or more forms
            have the same attributes as the form you want to select, and its
            position on the page is the only way to uniquely identify it.
            Default is the first matching form (``nr=0``).

        :return: The selected form as a soup object. It can also be
            retrieved later with :func:`get_current_form`.
        """
        if isinstance(selector, bs4.element.Tag):
            if selector.name != "form":
                raise LinkNotFoundError
            self.__state.form = Form(selector)
        else:
            # nr is a 0-based index for consistency with mechanize
            found_forms = self.get_current_page().select(selector,
                                                         limit=nr + 1)
            if len(found_forms) != nr + 1:
                if self.__debug:
                    print('select_form failed for', selector)
                    self.launch_browser()
                raise LinkNotFoundError()
            self.__state.form = Form(found_forms[-1])

        return self.get_current_form()

    def submit_selected(self, btnName=None, *args, **kwargs):
        """Submit the form that was selected with :func:`select_form`.

        :return: Forwarded from :func:`Browser.submit`.

        If there are multiple submit input/button elements, passes ``btnName``
        to :func:`Form.choose_submit` on the current form to choose between
        them. All other arguments are forwarded to :func:`Browser.submit`.
        """
        self.get_current_form().choose_submit(btnName)

        referer = self.get_url()
        if referer is not None:
            if 'headers' in kwargs:
                kwargs['headers']['Referer'] = referer
            else:
                kwargs['headers'] = {'Referer': referer}

        resp = self.submit(self.__state.form, url=self.__state.url,
                           *args, **kwargs)
        self.__state = _BrowserState(page=resp.soup, url=resp.url,
                                     request=resp.request)
        return resp

    def list_links(self, *args, **kwargs):
        """Display the list of links in the current page. Arguments are
        forwarded to :func:`links`.
        """
        print("Links in the current page:")
        for l in self.links(*args, **kwargs):
            print("    ", l)

    def links(self, url_regex=None, link_text=None, *args, **kwargs):
        """Return links in the page, as a list of bs4.element.Tag objects.

        To return links matching specific criteria, specify ``url_regex``
        to match the *href*-attribute, or ``link_text`` to match the
        *text*-attribute of the Tag. All other arguments are forwarded to
        the `.find_all() method in BeautifulSoup
        <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all>`__.
        """
        all_links = self.get_current_page().find_all(
            'a', href=True, *args, **kwargs)
        if url_regex is not None:
            all_links = [a for a in all_links
                         if re.search(url_regex, a['href'])]
        if link_text is not None:
            all_links = [a for a in all_links
                         if a.text == link_text]
        return all_links

    def find_link(self, *args, **kwargs):
        """Find and return a link, as a bs4.element.Tag object.

        The search can be refined by specifying any argument that is accepted
        by :func:`links`. If several links match, return the first one found.

        If no link is found, raise :class:`LinkNotFoundError`.
        """
        links = self.links(*args, **kwargs)
        if len(links) == 0:
            raise LinkNotFoundError()
        else:
            return links[0]

    def _find_link_internal(self, link, args, kwargs):
        """Wrapper around find_link that deals with convenience special-cases:

        * If ``link`` has an *href*-attribute, then return it. If not,
          consider it as a ``url_regex`` argument.

        * If searching for the link fails and debug is active, launch
          a browser.
        """
        if hasattr(link, 'attrs') and 'href' in link.attrs:
            return link

        # Check if "link" parameter should be treated as "url_regex"
        # but reject obtaining it from both places.
        if link and 'url_regex' in kwargs:
            raise ValueError('link parameter cannot be treated as '
                             'url_regex because url_regex is already '
                             'present in keyword arguments')
        else:
            kwargs['url_regex'] = link

        try:
            return self.find_link(*args, **kwargs)
        except LinkNotFoundError:
            if self.get_debug():
                print('find_link failed for', kwargs)
                self.list_links()
                self.launch_browser()
            raise

    def follow_link(self, link=None, *args, **kwargs):
        """Follow a link.

        If ``link`` is a bs4.element.Tag (i.e. from a previous call to
        :func:`links` or :func:`find_link`), then follow the link.

        If ``link`` doesn't have a *href*-attribute or is None, treat
        ``link`` as a url_regex and look it up with :func:`find_link`.
        Any additional arguments specified are forwarded to this function.

        If the link is not found, raise :class:`LinkNotFoundError`.
        Before raising, if debug is activated, list available links in the
        page and launch a browser.

        :return: Forwarded from :func:`open_relative`.
        """
        link = self._find_link_internal(link, args, kwargs)

        referer = self.get_url()
        headers = {'Referer': referer} if referer else None

        return self.open_relative(link['href'], headers=headers)

    def download_link(self, link=None, file=None, *args, **kwargs):
        """Downloads the contents of a link to a file. This function behaves
        similarly to :func:`follow_link`, but the browser state will
        not change when calling this function.

        :param file: Filesystem path where the page contents will be
            downloaded. If the file already exists, it will be overwritten.

        Other arguments are the same as :func:`follow_link` (``link``
        can either be a bs4.element.Tag or a URL regex, other
        arguments are forwarded to :func:`find_link`).

        :return: `requests.Response
            <http://docs.python-requests.org/en/master/api/#requests.Response>`__
            object.
        """
        link = self._find_link_internal(link, args, kwargs)
        url = self.absolute_url(link['href'])

        referer = self.get_url()
        headers = {'Referer': referer} if referer else None

        response = self.session.get(url, headers=headers)
        if self.raise_on_404 and response.status_code == 404:
            raise LinkNotFoundError()

        # Save the response content to file
        if file is not None:
            with open(file, 'wb') as f:
                f.write(response.content)

        return response

    def launch_browser(self, soup=None):
        """Launch a browser to display a page, for debugging purposes.

        :param: soup: Page contents to display, supplied as a bs4 soup object.
            Defaults to the current page of the ``StatefulBrowser`` instance.
        """
        if soup is None:
            soup = self.get_current_page()
        super(StatefulBrowser, self).launch_browser(soup)
