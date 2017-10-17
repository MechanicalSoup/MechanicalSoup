Frequently Asked Questions
==========================

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
