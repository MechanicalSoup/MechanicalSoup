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

From `<examples/expl_duck_duck_go.py>`__, code to get the results from
a DuckDuckGo search:

.. code:: python

    """Example usage of MechanicalSoup to get the results from
    DuckDuckGo."""
    
    import mechanicalsoup
    
    # Connect to duckduckgo
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://duckduckgo.com/")
    
    # Fill-in the search form
    browser.select_form('#search_form_homepage')
    browser["q"] = "MechanicalSoup"
    browser.submit_selected()
    
    # Display the results
    for l in browser.get_current_page().select('a.result__a'):
        print(l.text, '->', l.attrs['href'])

More examples are available in `<examples/>`__.

For an example with a more complex form (checkboxes, radio buttons and
textareas), read `<tests/test_browser.py>`__
and `<tests/test_form.py>`__.

Development
-----------

|Build Status| |Coverage Status|
|Requirements Status| |Documentation Status|

Instructions for building, testing and contributing to MechanicalSoup:
see `<CONTRIBUTING.rst>`__.

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
.. |Build Status| image:: https://travis-ci.org/MechanicalSoup/MechanicalSoup.svg?branch=master
   :target: https://travis-ci.org/MechanicalSoup/MechanicalSoup
.. |Coverage Status| image:: https://codecov.io/gh/MechanicalSoup/MechanicalSoup/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/MechanicalSoup/MechanicalSoup
.. |Requirements Status| image:: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements.svg?branch=master
   :target: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements/?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/mechanicalsoup/badge/?version=latest
   :target: http://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
