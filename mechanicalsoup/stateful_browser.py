from __future__ import print_function

from six.moves import urllib
from .browser import Browser
from .utils import LinkNotFoundError
from .form import Form
import sys
import re


class StatefulBrowser(Browser):
    def __init__(self, session=None, soup_config=None, requests_adapters=None,
                 *args, **kwargs):
        super(StatefulBrowser, self).__init__(
            session, soup_config, requests_adapters, *args, **kwargs)
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

        * >= 1 shows each visited URL."""
        self.__verbose = verbose

    def get_url(self):
        """Get the URL of the currently visited page."""
        return self.__current_url

    def get_current_form(self):
        """Get the currently selected form. See select_form()."""
        return self.__current_form

    def __setitem__(self, name, value):
        """Call item assignment on the currently selected form."""
        self.get_current_form()[name] = value

    def new_control(self, type, name, value, **kwargs):
        """Call new_control() on the currently selected form."""
        return self.get_current_form().new_control(type, name, value, **kwargs)

    def get_current_page(self):
        """Get the current page as a soup object."""
        return self.__current_page

    def absolute_url(self, url):
        """Make url absolute. url can be either relative or absolute."""
        return urllib.parse.urljoin(self.__current_url, url)

    def open(self, url, *args, **kwargs):
        """Open the URL in this Browser object."""
        if self.__verbose == 1:
            sys.stdout.write('.')
            sys.stdout.flush()
        elif self.__verbose >= 2:
            print(url)

        resp = self.get(url, *args, **kwargs)
        if hasattr(resp, 'soup'):
            self.__current_page = resp.soup
        self.__current_url = resp.url
        self.__current_form = None
        return resp

    def open_relative(self, url, *args, **kwargs):
        """Like open, but URL can be relative to the currently visited page."""
        return self.open(self.absolute_url(url))

    def select_form(self, *args, **kwargs):
        """Select a form in the current page. Arguments are the same
        as the select() method for a soup object."""
        found_forms = self.__current_page.select(*args, **kwargs)
        if len(found_forms) < 1:
            if self.__debug:
                print('select_form failed for', *args)
                self.launch_browser()
            raise LinkNotFoundError()

        self.__current_form = Form(found_forms[0])
        return self.__current_form

    def submit_selected(self, btnName=None, *args, **kwargs):
        """Submit the form selected with select_form()."""
        if btnName is not None:
            if 'data' not in kwargs:
                kwargs['data'] = dict()
            kwargs['data'][btnName] = ''

        form = self.get_current_form()
        if "action" in form.form:
            url = self.__current_url
        else:
            url = self.absolute_url(form.form["action"])
        resp = self.submit(self.__current_form,
                           url=url,
                           *args, **kwargs)
        self.__current_url = resp.url
        if hasattr(resp, "soup"):
            self.__current_page = resp.soup
        self.__current_form = None
        return resp

    def list_links(self, *args, **kwargs):
        """Display the list of links in the current page."""
        print("Links in the current page:")
        for l in self.links(*args, **kwargs):
            print("    ", l)

    def links(self, url_regex=None, link_text=None, *args, **kwargs):
        """Return links in the page, as a list of bs4.element.Tag object."""
        all_links = self.get_current_page().find_all(
            'a', href=True, *args, **kwargs)
        if url_regex is not None:
            all_links = [a for a in all_links
                         if re.search(url_regex, a['href'])]
        if link_text is not None:
            all_links = [a for a in all_links
                         if a.text == link_text]
        return all_links

    def find_link(self, url_regex=None, *args, **kwargs):
        """Find a link whose href property matches url_regex.

        If several links match, return the first one found.

        If url_regex is None, return the first link found on the page."""
        links = self.links(url_regex, *args, **kwargs)
        if len(links) == 0:
            raise LinkNotFoundError()
        else:
            return links[0]

    def follow_link(self, url_regex=None, *args, **kwargs):
        """Find a link whose href property matches url_regex, and follow it.

        If the link is not found, Raise LinkNotFoundError.
        Before raising LinkNotFoundError, if debug is activated, list
        available links in the page and launch a browser."""
        try:
            link = self.find_link(url_regex, *args, **kwargs)
            return self.open(self.absolute_url(link['href']))
        except LinkNotFoundError:
            if self.get_debug():
                print('follow_link failed for', url_regex)
                self.list_links()
                self.launch_browser()
            raise

    def launch_browser(self):
        """Launch a browser on the page, for debugging purpose."""
        super(StatefulBrowser, self).launch_browser(self.get_current_page())
