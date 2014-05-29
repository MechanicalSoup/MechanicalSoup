MechanicalSoup
==============

A Python library for automating interaction with websites. MechanicalSoup automatically stores and sends cookies, follows redirects, and can follow links and submit forms.

Rationale
------

WWW-Mechanize and Mechanize are the names of similar [Perl](http://search.cpan.org/dist/WWW-Mechanize/) and [Ruby](https://github.com/sparklemotion/mechanize) libraries. Unfortunately, their [Python sister project](https://github.com/jjlee/mechanize) has become inactive, and is now [incompatible with](https://github.com/jjlee/mechanize/issues/96) the most recent Python release, Python 3. This library provides a similar API, built on Python giants [Requests](http://docs.python-requests.org/en/latest/) (for http sessions) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) (for document navigation).
