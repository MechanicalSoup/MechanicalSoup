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

Some versions of BeautifulSoup show a harmless warning to encourage
you to specify which HTML parser to use. In MechanicalSoup 0.9, the
default parser is set by MechanicalSoup, so you shouldn't get the
error anymore (or you should upgrade) unless you specified a
non-standard `soup_config` argument to the browser's constructor.

If you specify a `soup_config` argument, you should include the parser
to use, like::

    mechanicalsoup.StatufulBrowser(soup_config={'features': 'lxml', '...': '...'})

Or if you don't have the parser `lxml
<http://lxml.de/installation.html>`__ installed::

    mechanicalsoup.StatefulBrowser(soup_config={'features': 'parser.html', ...})

See also
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#you-need-a-parser

How do I get debug information/logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To understand what's going on while running a script, you have two
options:

* Use :func:`~mechanicalsoup.StatefulBrowser.set_verbose` to set the
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

Should I use Browser or StatefulBrowser?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Short answer: :class:`mechanicalsoup.StatefulBrowser`.

:class:`mechanicalsoup.Browser` is historically the first class that
was introduced in Mechanicalsoup. Using it is a bit verbose, as the
caller needs to store the URL of the currently visited page and
manipulate the current form with a separate
variable. :class:`mechanicalsoup.StatefulBrowser` is essentially a
superset of :class:`mechanicalsoup.Browser`, it's the one you should
use unless you have a good reason to do otherwise.

How does MechanicalSoup compare to the alternatives?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are other libraries with the same purpose as MechanicalSoup:

* `Mechanize <http://wwwsearch.sourceforge.net/mechanize/>`__ is an
  ancestor of MechanicalSoup (getting its name from the Perl mechanize
  module). It was a great tool, but doesn't support Python 3. It was
  unmaintained for several years but got a new maintainer in 2017.
  Note that Mechanize is a much bigger piece of code (around 20 times
  more lines!) than MechanicalSoup, which is small because it
  delegates most of its work to BeautifulSoup and requests.

* `RoboBrowser <https://github.com/jmcarp/robobrowser>`__ is very
  similar to MechanicalSoup. Both are small libraries built on top of
  requests and BeautifulSoup. Their APIs are very similar. Both have an
  automated testsuite. As of writing, MechanicalSoup is more actively
  maintained (only 1 really active developer and no activity the last
  two years for RoboBrowser).

* `Selenium <http://selenium-python.readthedocs.io/>`__ is a much
  heavier solution: it launches a real web browser (Firefox,
  Chrome, ...) and controls it with inter-process communication.
  Selenium is the right solution if you want to test that a website
  works properly with various browsers (e.g. is the JavaScript code
  you're writing compatible with all major browsers on the market?),
  and is generally useful when you need JavaScript support.
  Though MechanicalSoup does not support JavaScript, it also does not
  have the overhead of a real web browser, which makes it a simple and
  efficient solution for basic website interactions.

"ReferenceError: weakly-referenced object no longer exists"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This error can occur within requests' ``session.py`` when called by
the destructor (``__del__``) of browser. The solution is to
call :func:`~mechanicalsoup.Browser.close` before the end of life of
the object.

Alternatively, you may also use the ``with`` statement which closes
the browser for you::

  def test_with():
      with mechanicalsoup.StatefulBrowser() as browser:
          browser.open(url)
          # ...
      # implicit call to browser.close() here.

This problem is fixed in MechanicalSoup 0.10, so this is only required
for compatibility with older versions. Code using new versions can let
the ``browser`` variable go out of scope and let the garbage collector
close it properly.
