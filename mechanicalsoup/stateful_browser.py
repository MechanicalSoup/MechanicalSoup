from __future__ import print_function

from six.moves import urllib
from .browser import Browser
from .utils import LinkNotFoundError
from .form import Form
import sys


class StatefulBrowser(Browser):
    def __init__(self, session=None, soup_config=None, requests_adapters=None):
        super(StatefulBrowser, self).__init__(
            session, soup_config, requests_adapters)
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
        self.__current_page = resp.soup
        self.__current_form = None
        return resp

    def launch_browser(self):
        """Launch a browser on the page, for debugging purpose."""
        super(StatefulBrowser, self).launch_browser(self.get_current_page())
