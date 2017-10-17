MechanicalSoup
==============

Home page
---------

http://mechanicalsoup.readthedocs.io/en/latest/

Overview
--------

A Python library for automating interaction with websites.
MechanicalSoup automatically stores and sends cookies, follows
redirects, and can follow links and submit forms. It doesn't do
Javascript.

MechanicalSoup was created by `M
Hickford <https://github.com/hickford/>`__, who was a fond user of the
`Mechanize <https://github.com/jjlee/mechanize>`__ library.
Unfortunately, Mechanize is `incompatible with Python
3 <https://github.com/jjlee/mechanize/issues/96>`__ and its development
is inactive. MechanicalSoup provides a similar API, built on Python
giants `Requests <http://docs.python-requests.org/en/latest/>`__ (for
http sessions) and
`BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`__ (for
document navigation). Since 2017 it is a project actively maintained by
a small team including @hemberger and @moy.

Installation
------------

|Latest Version| |Supported Versions|

From `PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__

::

     pip install MechanicalSoup

PyPy and PyPy3 are also supported (and tested against).

Documentation
-------------

The full documentation is available on
http://mechanicalsoup.readthedocs.io/. You may want to jump directly to
the `automaticaly generated API
documentation <http://mechanicalsoup.readthedocs.io/en/latest/mechanicalsoup.html>`__.

Example
-------

From ```example.py`` <example.py>`__, code to log into the GitHub
website:

.. code:: python

    """Example app to login to GitHub using the StatefulBrowser class."""

    from __future__ import print_function
    import argparse
    import mechanicalsoup
    from getpass import getpass

    parser = argparse.ArgumentParser(description="Login to GitHub.")
    parser.add_argument("username")
    args = parser.parse_args()

    args.password = getpass("Please enter your GitHub password: ")

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )
    # Uncomment for a more verbose output:
    # browser.set_verbose(2)

    browser.open("https://github.com")
    browser.follow_link("login")
    browser.select_form('#login form')
    browser["login"] = args.username
    browser["password"] = args.password
    resp = browser.submit_selected()

    # Uncomment to launch a web browser on the current page:
    # browser.launch_browser()

    # verify we are now logged in
    page = browser.get_current_page()
    messages = page.find("div", class_="flash-messages")
    if messages:
        print(messages.text)
    assert page.select(".logout-form")

    print(page.title.text)

    # verify we remain logged in (thanks to cookies) as we browse the rest of
    # the site
    page3 = browser.open("https://github.com/MechanicalSoup/MechanicalSoup")
    assert page3.soup.select(".logout-form")

For an example with a more complex form (checkboxes, radio buttons and
textareas), read ```tests/test_browser.py`` <tests/test_browser.py>`__
and ```tests/test_form.py`` <tests/test_form.py>`__.

Common problems
---------------

"No parser was explicitly specified"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    UserWarning: No parser was explicitly specified, so I'm using the
    best available HTML parser for this system ("lxml"). This usually
    isn't a problem, but if you run this code on another system, or in a
    different virtual environment, it may use a different parser and
    behave differently.

Recent versions of BeautifulSoup show a harmless warning to encourage
you to specify which HTML parser to use. You can do this in
MechanicalSoup:

::

    mechanicalsoup.Browser(soup_config={'features':'html.parser'})

Or if you have the parser `lxml <http://lxml.de/installation.html>`__
installed:

::

    mechanicalsoup.Browser(soup_config={'features':'lxml'})

See also
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#you-need-a-parser

Development
-----------

|Build Status| |Coverage Status| |Requirements Status| |Documentation
Status|

Python version support in the current master branch may differ from the
latest release in
`PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__. Please inspect
``.travis.yml`` or run ``python setup.py --classifiers`` to see which
versions of Python are supported in the current master branch.

Installing dependencies and running tests can be done with:

::

    python setup.py test

The documentation can be generated and viewed with:

::

    pip install sphinx
    python setup.py build_sphinx
    firefox docs/_build/html/index.html

The documentation is generated from docstrings within ``*.py`` files,
and ``*.rst`` documentation files in the ``docs/`` directory.

You can develop against multiple versions of Python using
`virtualenv <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>`__:

::

    python3 -m venv .virtual-py3 && source .virtual-py3/bin/activate
    pip install -r requirements.txt -r tests/requirements.txt

and

::

    virtualenv -p python2 --no-site-packages .virtual-py2 && source .virtual-py2/bin/activate
    pip install -r requirements.txt -r tests/requirements.txt

After making changes, run pytest in all virtualenvs:

::

    source .virtual-py3/bin/activate
    pytest

    source .virtual-py2/bin/activate
    pytest

Installation should be as simple as:

::

    python setup.py install

Roadmap
~~~~~~~

-  Draw `Substack-style <http://substack.net/art>`__ readme art (imagine
   a steaming bowl of cogs and noodles)
-  `Write docs and publish
   website <https://github.com/MechanicalSoup/MechanicalSoup/issues/6>`__

See also
--------

-  `RoboBrowser <https://github.com/jmcarp/robobrowser>`__: a similar
   library, also based on Requests and BeautifulSoup.
-  `Hacker News post <https://news.ycombinator.com/item?id=8012103>`__
-  `Reddit
   discussion <http://www.reddit.com/r/programming/comments/2aa13s/mechanicalsoup_a_python_library_for_automating/>`__

.. |Latest Version| image:: https://img.shields.io/pypi/v/MechanicalSoup.svg
   :target: https://pypi.python.org/pypi/MechanicalSoup/
.. |Supported Versions| image:: https://img.shields.io/pypi/pyversions/mechanicalsoup.svg
   :target: https://pypi.python.org/pypi/MechanicalSoup/
.. |Build Status| image:: https://travis-ci.org/MechanicalSoup/MechanicalSoup.svg?branch=master
   :target: https://travis-ci.org/MechanicalSoup/MechanicalSoup
.. |Coverage Status| image:: https://codecov.io/gh/MechanicalSoup/MechanicalSoup/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/MechanicalSoup/MechanicalSoup
.. |Requirements Status| image:: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements.svg?branch=master
   :target: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements/?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/mechanicalsoup/badge/?version=latest
   :target: http://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
