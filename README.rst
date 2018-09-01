.. image:: /assets/mechanical-soup-logo.png
   :alt: MechanicalSoup. A Python library for automating website
	 interaction.

Home page
---------

https://mechanicalsoup.readthedocs.io/

Overview
--------

A Python library for automating interaction with websites.
MechanicalSoup automatically stores and sends cookies, follows
redirects, and can follow links and submit forms. It doesn't do
JavaScript.

MechanicalSoup was created by `M Hickford
<https://github.com/hickford/>`__, who was a fond user of the
`Mechanize <https://github.com/jjlee/mechanize>`__ library.
Unfortunately, Mechanize is `incompatible with Python 3
<https://github.com/jjlee/mechanize/issues/96>`__ and its development
stalled for several years. MechanicalSoup provides a similar API, built on Python
giants `Requests <http://docs.python-requests.org/en/latest/>`__ (for
HTTP sessions) and `BeautifulSoup
<https://www.crummy.com/software/BeautifulSoup/>`__ (for document
navigation). Since 2017 it is a project actively maintained by a small
team including `@hemberger <https://github.com/hemberger>`__ and `@moy
<https://github.com/moy/>`__.

|Gitter Chat|

Installation
------------

|Latest Version| |Supported Versions|

PyPy and PyPy3 are also supported (and tested against).

Download and install the latest released version from `PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__::

  pip install MechanicalSoup

Download and install the development version from `GitHub <https://github.com/MechanicalSoup/MechanicalSoup>`__::

  pip install git+https://github.com/MechanicalSoup/MechanicalSoup

Installing from source (installs the version in the current working directory)::

  python setup.py install

(In all cases, add ``--user`` to the ``install`` command to
install in the current user's home directory.)


Documentation
-------------

The full documentation is available on
https://mechanicalsoup.readthedocs.io/. You may want to jump directly to
the `automatically generated API
documentation <https://mechanicalsoup.readthedocs.io/en/latest/mechanicalsoup.html>`__.

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
    for link in browser.get_current_page().select('a.result__a'):
        print(link.text, '->', link.attrs['href'])

More examples are available in `<examples/>`__.

For an example with a more complex form (checkboxes, radio buttons and
textareas), read `<tests/test_browser.py>`__
and `<tests/test_form.py>`__.

Development
-----------

|Build Status| |Coverage Status|
|Requirements Status| |Documentation Status|
|CII Best Practices|
|LGTM Alerts|
|LGTM Grade|

Instructions for building, testing and contributing to MechanicalSoup:
see `<CONTRIBUTING.rst>`__.

Common problems
---------------

Read the `FAQ
<https://mechanicalsoup.readthedocs.io/en/latest/faq.html>`__.


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
   :target: https://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/1334/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/1334
.. |Gitter Chat| image:: https://badges.gitter.im/MechanicalSoup/MechanicalSoup.svg
   :target: https://gitter.im/MechanicalSoup/Lobby
.. |LGTM Alerts| image:: https://img.shields.io/lgtm/alerts/g/MechanicalSoup/MechanicalSoup.svg
   :target: https://lgtm.com/projects/g/MechanicalSoup/MechanicalSoup/
.. |LGTM Grade| image:: https://img.shields.io/lgtm/grade/python/g/MechanicalSoup/MechanicalSoup.svg
   :target: https://lgtm.com/projects/g/MechanicalSoup/MechanicalSoup/
