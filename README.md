MechanicalSoup
==============

A Python library for automating interaction with websites. MechanicalSoup automatically stores and sends cookies, follows redirects, and can follow links and submit forms.

Installation
------

[![Latest Version](https://pypip.in/version/MechanicalSoup/badge.svg)](https://pypi.python.org/pypi/MechanicalSoup/)

From [PyPI](https://pypi.python.org/pypi/MechanicalSoup/)

     pip install MechanicalSoup
    

Rationale
------

WWW-Mechanize and Mechanize are similar [Perl](http://search.cpan.org/dist/WWW-Mechanize/) and [Ruby](https://github.com/sparklemotion/mechanize) libraries. Unfortunately, their [Python sister project](https://github.com/jjlee/mechanize) has become inactive, and is now [incompatible with](https://github.com/jjlee/mechanize/issues/96) recent Python versions (Python 3.x). This library provides a similar API, built on Python giants [Requests](http://docs.python-requests.org/en/latest/) (for http sessions) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) (for document navigation).

Example
------

From [`example.py`](example.py), code to log into the GitHub website:

    import mechanicalsoup

    browser = mechanicalsoup.Browser()

    # request github login page
    login_page = browser.get("https://github.com/login")

    # find login form
    login_form = login_page.soup.select("#login")[0].select("form")[0]

    # specify username and password
    login_form.select("#login_field")[0]['value'] = "username"
    login_form.select("#password")[0]['value'] = "password"

    # submit form
    page2 = browser.submit(login_form, login_page.response.url)

    # verify we are now logged in
    assert page2.soup.select(".logout-form")

    # verify we remain logged in (thanks to cookies) as we browse the rest of the site
    page3 = browser.get("https://github.com/colonelpanic/MechanicalSoup")
    assert page3.soup.select(".logout-form")

For an example with a more complicated form (with checkboxes, radio buttons and textareas), read [`tests/test_browser.py`](tests/test_browser.py).

Development
---------

[![Build Status](https://travis-ci.org/colonelpanic/MechanicalSoup.svg?branch=master)](https://travis-ci.org/colonelpanic/MechanicalSoup)

### Tests

    py.test
