MechanicalSoup
==============

A Python library for automating interaction with websites. MechanicalSoup automatically stores and sends cookies, follows redirects, and can follow links and submit forms.

Rationale
------

WWW-Mechanize and Mechanize are similar [Perl](http://search.cpan.org/dist/WWW-Mechanize/) and [Ruby](https://github.com/sparklemotion/mechanize) libraries. Unfortunately, their [Python sister project](https://github.com/jjlee/mechanize) has become inactive, and is now [incompatible with](https://github.com/jjlee/mechanize/issues/96) recent Python versions (Python 3.x). This library provides a similar API, built on Python giants [Requests](http://docs.python-requests.org/en/latest/) (for http sessions) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) (for document navigation).

Development
---------

[![Build Status](https://travis-ci.org/matt-hickford/MechanicalSoup.svg?branch=master)](https://travis-ci.org/matt-hickford/MechanicalSoup)
