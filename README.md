MechanicalSoup
==============

A Python library for automating interaction with websites. MechanicalSoup automatically stores and sends cookies, follows redirects, and can follow links and submit forms. It doesn't do Javascript.

I was a fond user of the [Mechanize](https://github.com/jjlee/mechanize) library, but unfortunately it's  [incompatible with Python 3](https://github.com/jjlee/mechanize/issues/96) and development is inactive. MechanicalSoup provides a similar API, built on Python giants [Requests](http://docs.python-requests.org/en/latest/) (for http sessions) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) (for document navigation).

Installation
------

[![Latest Version](https://img.shields.io/pypi/v/MechanicalSoup.svg)](https://pypi.python.org/pypi/MechanicalSoup/)

From [PyPI](https://pypi.python.org/pypi/MechanicalSoup/)

     pip install MechanicalSoup

Python versions 2.6-2.7, 3.3-3.6, PyPy and PyPy3 are supported (and tested against).

Example
------

From [`example.py`](example.py), code to log into the GitHub website:

```python
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
page3 = browser.open("https://github.com/hickford/MechanicalSoup")
assert page3.soup.select(".logout-form")
```

For an example with a more complex form (checkboxes, radio buttons and textareas), read [`tests/test_browser.py`](tests/test_browser.py) and [`tests/test_form.py`](tests/test_form.py).

Common problems
---

### "No parser was explicitly specified"

> UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

Recent versions of BeautifulSoup show a harmless warning to encourage you to specify which HTML parser to use. You can do this in MechanicalSoup:

    mechanicalsoup.Browser(soup_config={'features':'html.parser'})

Or if you have the parser [lxml](http://lxml.de/installation.html) installed:

    mechanicalsoup.Browser(soup_config={'features':'lxml'})

See also https://www.crummy.com/software/BeautifulSoup/bs4/doc/#you-need-a-parser

Development
---------

[![Build Status](https://travis-ci.org/hickford/MechanicalSoup.svg?branch=master)](https://travis-ci.org/hickford/MechanicalSoup)

### Tests

    py.test

### Roadmap

* Draw [Substack-style](http://substack.net/art) readme art (imagine a steaming bowl of cogs and noodles)
* [Write docs and publish website](https://github.com/hickford/MechanicalSoup/issues/6)

See also
------

* [RoboBrowser](https://github.com/jmcarp/robobrowser): a similar library, also based on Requests and BeautifulSoup.
* [Hacker News post](https://news.ycombinator.com/item?id=8012103)
* [Reddit discussion](http://www.reddit.com/r/programming/comments/2aa13s/mechanicalsoup_a_python_library_for_automating/)
