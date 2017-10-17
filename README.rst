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

PyPy and PyPy3 are also supported (and tested against).

From `PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__::

     pip install MechanicalSoup

Installing from source::

  python setup.py install

(In both cases, add ``--user`` to install in the current user's home directory)


Documentation
-------------

The full documentation is available on
http://mechanicalsoup.readthedocs.io/. You may want to jump directly to
the `automaticaly generated API
documentation <http://mechanicalsoup.readthedocs.io/en/latest/mechanicalsoup.html>`__.

Example
-------

From `example.py <example.py>`__, code to log into the GitHub
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
textareas), read `tests/test_browser.py <tests/test_browser.py>`__
and `tests/test_form.py <tests/test_form.py>`__.

Common problems
---------------

Read the `FAQ
<http://mechanicalsoup.readthedocs.io/en/latest/faq.html>`__.

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
