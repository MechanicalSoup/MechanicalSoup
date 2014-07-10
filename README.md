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

```python
"""Example app to login to GitHub"""
import argparse
import mechanicalsoup

parser = argparse.ArgumentParser(description='Login to GitHub.')
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

browser = mechanicalsoup.Browser()

# request github login page. the result is a requests.Response object http://docs.python-requests.org/en/latest/user/quickstart/#response-content
login_page = browser.get("https://github.com/login")

# login_page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup 
# we grab the login form
login_form = login_page.soup.select("#login")[0].select("form")[0]

# specify username and password
login_form.select("#login_field")[0]['value'] = args.username
login_form.select("#password")[0]['value'] = args.password

# submit form
page2 = browser.submit(login_form, login_page.url)

# verify we are now logged in
messages = page2.soup.find('div', class_='flash-messages')
if messages:
    print(messages.text)
assert page2.soup.select(".logout-form")

print(page2.soup.title.text)

# verify we remain logged in (thanks to cookies) as we browse the rest of the site
page3 = browser.get("https://github.com/matt-hickford/MechanicalSoup")
assert page3.soup.select(".logout-form")
```

For an example with a more complicated form (with checkboxes, radio buttons and textareas), read [`tests/test_browser.py`](tests/test_browser.py).

Development
---------

[![Build Status](https://travis-ci.org/hickford/MechanicalSoup.svg?branch=master)](https://travis-ci.org/hickford/MechanicalSoup)

### Tests

    py.test
