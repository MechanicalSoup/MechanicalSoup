from __future__ import print_function

from six.moves import urllib
from .browser import Browser
from .utils import LinkNotFoundError
from .form import Form
import sys
import re
import bs4


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

    Once not used anymore, the browser must be closed
    using :func:`~Browser.close`.
    """

    def __init__(self, *args, **kwargs):
        super(StatefulBrowser, self).__init__(*args, **kwargs)
        self.__debug = False
        self.__verbose = 0
        self.__current_page = None
        self.__current_url = None
        self.__current_form = None

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
        return self.__current_url

    def get_current_form(self):
        """Get the currently selected form as a :class:`Form` object.
        See :func:`select_form`.
        """
        return self.__current_form

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
        return self.__current_page

    def absolute_url(self, url):
        """Return the absolute URL made from the current URL and ``url``.
        The current URL is only used to provide any missing components of
        ``url``, as in the `.urljoin() method of urllib.parse
        <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin>`__.
        """
        return urllib.parse.urljoin(self.__current_url, url)

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
        self.__current_page = resp.soup
        self.__current_url = resp.url
        self.__current_form = None
        return resp

    def open_fake_page(self, page_text, url=None, soup_config=None):
        """Mock version of :func:`open`.

        Behave as if opening a page whose text is ``page_text``, but do not
        perform any network access. If ``url`` is set, pretend it is the page's
        URL. Useful mainly for testing.
        """
        soup_config = soup_config or self.soup_config
        self.__current_page = bs4.BeautifulSoup(
            page_text, **soup_config)
        self.__current_url = url
        self.__current_form = None

    def open_relative(self, url, *args, **kwargs):
        """Like :func:`open`, but ``url`` can be relative to the currently
        visited page.
        """
        return self.open(self.absolute_url(url), *args, **kwargs)

    def select_form(self, selector="form", nr=0):
        """Select a form in the current page.

        :param selector: CSS selector to identify the form to select.
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
        # nr is a 0-based index for consistency with mechanize
        found_forms = self.__current_page.select(selector, limit=nr + 1)
        if len(found_forms) != nr + 1:
            if self.__debug:
                print('select_form failed for', selector)
                self.launch_browser()
            raise LinkNotFoundError()

        self.__current_form = Form(found_forms[-1])
        return self.__current_form

    def submit_selected(self, btnName=None, *args, **kwargs):
        """Submit the form that was selected with :func:`select_form`.

        :return: Forwarded from :func:`Browser.submit`.

        If there are multiple submit input/button elements, passes ``btnName``
        to :func:`Form.choose_submit` on the current form to choose between
        them. All other arguments are forwarded to :func:`Browser.submit`.
        """
        if btnName is not None:
            self.get_current_form().choose_submit(btnName)

        resp = self.submit(self.__current_form,
                           url=self.__current_url,
                           *args, **kwargs)
        self.__current_url = resp.url
        self.__current_page = resp.soup
        self.__current_form = None
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
        if not hasattr(link, 'attrs') or 'href' not in link.attrs:
            try:
                link = self.find_link(link, *args, **kwargs)
            except LinkNotFoundError:
                if self.get_debug():
                    print('follow_link failed for', link)
                    self.list_links()
                    self.launch_browser()
                raise
        return self.open_relative(link['href'])

    def launch_browser(self):
        """Launch a browser on the page, for debugging purposes."""
        super(StatefulBrowser, self).launch_browser(self.get_current_page())
