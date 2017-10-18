Frequently Asked Questions
==========================

When to use MechanicalSoup?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

MechanicalSoup is designed to simulate the behavior of a human using a
web browser. Possible use-case include:

* Interacting with a website that doesn't provide a webservice API,
  out of a browser.

* Testing a website you're developing

There are also situations when you should *not* use MechanicalSoup,
like:

* If the website provides a webservice API (e.g. REST), then you
  should use this API and you don't need MechanicalSoup.

* If the website you're interacting with does not contain HTML pages,
  then MechanicalSoup won't bring anything compared to `requests
  <http://docs.python-requests.org/>`__, so just use requests instead.

* If the website relies on JavaScript, then you probably need a
  fully-fledged browser. `Selenium <http://www.seleniumhq.org/>`__ may
  help you there, but it's a far heavier solution than MechanicalSoup.

* If the website is specifically designed to interact with humans,
  please don't go against the will of the website's owner.

"No parser was explicitly specified"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    UserWarning: No parser was explicitly specified, so I'm using the
    best available HTML parser for this system ("lxml"). This usually
    isn't a problem, but if you run this code on another system, or in a
    different virtual environment, it may use a different parser and
    behave differently.

Recent versions of BeautifulSoup show a harmless warning to encourage
you to specify which HTML parser to use. You can do this in
MechanicalSoup::

    mechanicalsoup.Browser(soup_config={'features':'html.parser'})

Or if you have the parser `lxml <http://lxml.de/installation.html>`__
installed::

    mechanicalsoup.Browser(soup_config={'features':'lxml'})

See also
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#you-need-a-parser

"ReferenceError: weakly-referenced object no longer exists"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This error can occure within requests' ``session.py`` when called by
the destructor (``__del__``) of browser. The solution is to
call :func:`~mechanicalsoup.Browser.close` before the end of life of
the object.

How do I get debug information/logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To unerstand what's going on while running a script, you have two
options:

* Use :func:`~mechanicalsoup.StatefulBrowser.set_debug` to set the
  debug level to 1 (show one dot for each page opened, a poor man's
  progress bar) or 2 (show the URL of each visited page).

* Activate request's logging::

    import requests
    import logging

    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

  This will display a much more verbose output, including HTTP status
  code for each page visited. Note that unlike MechanicalSoup's
  logging system, this includes URL returning a redirect (e.g. HTTP
  301), that are dealt with automatically by requests and not visible
  to MechanicalSoup.
