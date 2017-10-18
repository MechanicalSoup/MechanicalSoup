MechanicalSoup tutorial
=======================

First contact, step by step
---------------------------

As a simple example, we'll browse http://httpbin.org/, a website
designed to test tools like MechanicalSoup.

First, let's create a browser object::

  >>> import mechanicalsoup
  >>> browser = mechanicalsoup.StatefulBrowser()

To customize the way to build a browser (change the user-agent, the
HTML parser to use, the way to react to 404 Not Found errors, ...),
see :func:`~mechanicalsoup.StatefulBrowser.__init__`.

Now, open the webpage we want::

  >>> browser.open("http://httpbin.org/")
  <Response [200]>

The return value of :func:`~mechanicalsoup.StatefulBrowser.open` is an
object of type requests.Response_. Actually, MechanicalSoup is using
the requests_ library to do the actual requests to the website, so
there's no surprise that we're getting such object. In short, it
contains the data and meta-data that the server sent us. You see the
HTTP response status, 200, which means "OK", but the object also
contains the content of the page we just downloaded.

Just like a normal browser's URL bar, the browser remembers which URL
it's browsing::

  >>> browser.get_url()
  'http://httpbin.org/'

Now, let's follow the link to ``/forms/post``::

  >>> browser.follow_link("forms")
  <Response [200]>
  >>> browser.get_url()
  'http://httpbin.org/forms/post'

We passed a regular expression ``"forms"``
to :func:`~mechanicalsoup.StatefulBrowser.follow_link`, who followed
the link whose text matched this expression. There are many other ways
to call :func:`~mechanicalsoup.StatefulBrowser.follow_link`, but we'll
get back to it.

We're now visiting http://httpbin.org/forms/post, which contains a
form. Let's see the page content::

  >>> browser.get_current_page()
  <!DOCTYPE html>
  <html>
  ...
  <form action="/post" method="post">
  ...

Actually, the return type
of :func:`~mechanicalsoup.StatefulBrowser().get_current_page` is
bs4.BeautifulSoup_. BeautifulSoup, aka bs4, is the second library used
by Mechanicalsoup: it is an HTML manipulation library. You can now
navigate in the tags of the pages using BeautifulSoup. For example, to
get all the ``<legend>`` tags::

  >>> browser.get_current_page().find_all('legend')
  [<legend> Pizza Size </legend>, <legend> Pizza Toppings </legend>]

To fill-in a form, we need to tell MechanicalSoup which form we're
going to fill-in and submit::

  >>> browser.select_form('form[action="/post"]')

The argument to :func:`~mechanicalsoup.StatefulBrowser.select_form` is
a CSS selector. Here, we select an HTML tag named ``form`` having an
attribute ``action`` whose value is ``"/post"``. Since there's only
one form in the page, ``browser.select_form()`` would have done the
trick too.

Now, give a value to fields in the form. First, what are the available
fields? You can print a summary of the currently selected form
with :func:`~mechanicalsoup.Form.print_summary()`::

  >>> browser.get_current_form().print_summary()
  <input name="custname"/>
  <input name="custtel" type="tel"/>
  <input name="custemail" type="email"/>
  <input name="size" type="radio" value="small"/>
  <input name="size" type="radio" value="medium"/>
  <input name="size" type="radio" value="large"/>
  <input name="topping" type="checkbox" value="bacon"/>
  <input name="topping" type="checkbox" value="cheese"/>
  <input name="topping" type="checkbox" value="onion"/>
  <input name="topping" type="checkbox" value="mushroom"/>
  <input max="21:00" min="11:00" name="delivery" step="900" type="time"/>
  <textarea name="comments"></textarea>

For text fields, it's simple:
just give a value for ``input`` element based on their ``name``
attribute::

  >>> browser["custname"] = "Me"
  >>> browser["custtel"] = "00 00 0001"
  >>> browser["custemail"] = "nobody@example.com"
  >>> browser["comments"] = "This pizza looks really good :-)"

For radio buttons, well, it's simple too: radio buttons have several
``input`` tag with the same ``name`` and different values, just select
the one you need (``"size"`` is the ``name`` attribute, ``"medium"``
is the ``"value"`` attribute of the element we want to tick)::

  >>> browser["size"] = "medium"

For checkboxes, one can use the same mechanism to check one box::

  >>> browser["topping"] = "bacon"

But we can also check any number of boxes by assigning a list to the
field::

  >>> browser["topping"] = ("bacon", "cheese")

Actually, ``browser["..."] = "..."`` (i.e. calls
to :func:`~mechanicalsoup.StatefulBrowser.__setitem__`) is just a
helper to fill-in a form, but you can use any tool BeautifulSoup
provides to modify the soup object, and MechanicalSoup will take care
of submitting the form for you.

Let's see what the filled-in form looks like::

  >>> browser.launch_browser()

:func:`~mechanicalsoup.StatefulBrowser.launch_browser` will launch a
real web browser on the current page visited by our ``browser``
object, including the changes we just made to the form (note that it
does not open the real webpage, but creates a temporary file
containing the page content, and point your browser to this file). Try
changing the boxes ticked and the content of the text field, and
re-launch the browser.

This method is very useful in complement with your browser's web
development tools. For example, with Firefox, right-click "Inspect
Element" on a field will give you everything you need to manipulate
this field (in particular the ``name`` and ``value`` attributes).

It's also possible to check the content
with :func:`~mechanicalsoup.Form.print_summary()` (that we already
used to list the fields)::

  >>> browser.get_current_form().print_summary()
  <input name="custname" value="Me"/>
  <input name="custtel" type="tel" value="00 00 0001"/>
  <input name="custemail" type="email" value="nobody@example.com"/>
  <input name="size" type="radio" value="small"/>
  <input checked="" name="size" type="radio" value="medium"/>
  <input name="size" type="radio" value="large"/>
  <input checked="" name="topping" type="checkbox" value="bacon"/>
  <input checked="" name="topping" type="checkbox" value="cheese"/>
  <input name="topping" type="checkbox" value="onion"/>
  <input name="topping" type="checkbox" value="mushroom"/>
  <input max="21:00" min="11:00" name="delivery" step="900" type="time"/>
  <textarea name="comments">This pizza looks really good :-)</textarea>

Assuming we're satisfied with the content of the form, we can submit
it (i.e. simulate a click on the sumbit button)::

  >>> response = browser.submit_selected()

The response is not an HTML page, so the browser doesn't parse it to a
BeautifulSoup object, but we can still see the text it contains::

  >>> print(response.text)
  {
    "args": {},
    "data": "",
    "files": {},
    "form": {
      "comments": "This pizza looks really good :-)",
      "custemail": "nobody@example.com",
      "custname": "Me",
      "custtel": "00 00 0001",
      "delivery": "",
      "size": "medium",
      "topping": [
        "bacon",
        "cheese"
      ]
    },
  ...

To sum up, here is the complete example (`examples/expl_httpbin.py
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/examples/expl_httpbin.py>`__):

.. literalinclude:: ../examples/expl_httpbin.py

.. _requests: http://docs.python-requests.org/en/master/
.. _requests.Response: http://docs.python-requests.org/en/master/api/#requests.Response
.. _bs4.BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup

A more complete example: logging-in into GitHub
-----------------------------------------------

The simplest way to use MechanicalSoup is to use
the :class:`~mechanicalsoup.StatefulBrowser` class (this example is
available as `examples/example.py
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/examples/example.py>`__
in MechanicalSoup's source code):

.. literalinclude:: ../examples/example.py
   :language: python

Alternatively, one can use the :class:`~mechanicalsoup.Browser` class,
which doesn't maintain a state from one call to another (i.e. the
Browser itself doesn't remember which page you are visiting and what
is its content, it's up to the caller to do so). This example is
available as `examples/example_manual.py
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/examples/example_manual.py>`__
in the source:

.. literalinclude:: ../examples/example_manual.py
   :language: python

More examples
~~~~~~~~~~~~~

For more examples, see the `examples
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/examples/>`__
directory in MechanicalSoup's source code.
