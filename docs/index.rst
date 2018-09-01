.. MechanicalSoup documentation master file, created by
   sphinx-quickstart on Sun Sep 14 18:44:39 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../assets/mechanical-soup-logo.png
   :alt: MechanicalSoup. A Python library for automating website
	 interaction.
   :align: center

.. This '|' generates a blank line to avoid sticking the logo to the
   section.
|

Welcome to MechanicalSoup's documentation!
==========================================

A Python library for automating interaction with websites. MechanicalSoup automatically stores and sends cookies, follows redirects, and can follow links and submit forms. It doesn't do Javascript.

MechanicalSoup was created by `M Hickford
<https://github.com/hickford/>`__, who was a fond user of the
`Mechanize <https://github.com/jjlee/mechanize>`__ library.
Unfortunately, Mechanize is `incompatible with Python 3
<https://github.com/jjlee/mechanize/issues/96>`__ and its development
stalled for several years. MechanicalSoup provides a similar API, built on Python
giants `Requests <http://docs.python-requests.org/en/latest/>`__ (for
http sessions) and `BeautifulSoup
<http://www.crummy.com/software/BeautifulSoup/>`__ (for document
navigation). Since 2017 it is a project actively maintained by a small
team including `@hemberger <https://github.com/hemberger>`__ and `@moy
<https://github.com/moy/>`__.

Contents:

.. toctree::
   :maxdepth: 2

   introduction
   tutorial
   mechanicalsoup
   faq
   external-resources
   ChangeLog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

