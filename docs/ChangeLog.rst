=============
Release Notes
=============

Version 1.0 (in development)
============================

Main changes:
-------------

* ``StatefulBrowser`` methods ``get_current_page``,
  ``get_current_form`` and ``get_url`` have been deprecated in favor
  of ``page``, ``form`` and ``url`` properties (e.g. the new
  ``x.page`` is equivalent to the now deprecated
  ``x.get_current_page()``) [`#175
  <https://github.com/MechanicalSoup/MechanicalSoup/issues/175`__]

* ``StatefulBrowser.form`` will raise an ``AttributeError`` instead of
  returning ``None`` if no form has been selected yet. Note that
  ``StatefulBrowser.get_current_form()`` still returns ``None`` for
  backward compatibility.

* Added ability to submit a form without updating `StatefulBrowser` internal
  state. This means you get a response from the form submission, but your
  browser "stays" on the same page. Useful for handling forms that result in
  a download of a file or opening a new window.

Bug fixes
---------

* Form controls with the ``disabled`` attribute will no longer be submitted
  to improve compliance with the HTML standard. If you were relying on this
  bug to submit disabled elements, you can still achieve this by deleting the
  ``disabled`` attribute from the element in the :class:`~mechanicalsoup.Form`
  object directly.
  [`#248 <https://github.com/MechanicalSoup/MechanicalSoup/issues/248>`__]
* Upon submitting a form containing a file input field without uploading one,
  an empty filename & content will be sent in compliance with regular web
  browser behavior.
  [`#250 <https://github.com/MechanicalSoup/MechanicalSoup/issues/250>`__]

Version 0.11
============

This release focuses on fixing bugs related to uncommon HTTP/HTML
scenarios and on improving the documentation.

Bug fixes
---------

* Constructing a :class:`~mechanicalsoup.Form` instance from a
  ``bs4.element.Tag`` whose tag name is not ``form`` will now emit a warning,
  and may be deprecated in the future.
  [`#228 <https://github.com/MechanicalSoup/MechanicalSoup/pull/228>`__]

* **Breaking Change:** :class:`~mechanicalsoup.LinkNotFoundError` now derives
  from ``Exception`` instead of ``BaseException``. While this will bring the
  behavior in line with most people's expectations, it may affect the behavior
  of your code if you were heavily relying on this implementation detail in
  your exception handling.
  [`#203 <https://github.com/MechanicalSoup/MechanicalSoup/issues/203>`__]

* Improve handling of ``button`` submit elements. Will now correctly ignore
  buttons of type ``button`` and ``reset`` during form submission, since they
  are not considered to be submit elements.
  [`#199 <https://github.com/MechanicalSoup/MechanicalSoup/pull/199>`__]

* Do a better job of inferring the content type of a response if the
  ``Content-Type`` header is not provided.
  [`#195 <https://github.com/MechanicalSoup/MechanicalSoup/pull/195>`__]

* Improve consistency of query string construction between MechanicalSoup
  and web browsers in edge cases where form elements have duplicate name
  attributes. This prevents errors in valid use cases, and also makes
  MechanicalSoup more tolerant of invalid HTML.
  [`#158 <https://github.com/MechanicalSoup/MechanicalSoup/issues/158>`__]

Version 0.10
============

Main changes:
-------------
* Added ``StatefulBrowser.refresh()`` to reload the current page with the same request.
  [`#188 <https://github.com/MechanicalSoup/MechanicalSoup/issues/188>`__]

* ``StatefulBrowser.follow_link``,
  ``StatefulBrowser.submit_selected()`` and the new
  ``StatefulBrowser.download_link`` now sets the ``Referer:`` HTTP
  header to the page from which the link is followed.
  [`#179 <https://github.com/MechanicalSoup/MechanicalSoup/issues/179>`__]

* Added method ``StatefulBrowser.download_link``, which will download the
  contents of a link to a file without changing the state of the browser.
  [`#170 <https://github.com/MechanicalSoup/MechanicalSoup/issues/170>`__]

* The ``selector`` argument of ``Browser.select_form`` can now be a
  `bs4.element.Tag <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#tag>`__
  in addition to a CSS selector.
  [`#169 <https://github.com/MechanicalSoup/MechanicalSoup/issues/169>`__]

* ``Browser.submit`` and ``StatefulBrowser.submit_selected`` accept a larger
  number of keyword arguments. Arguments are forwarded to
  `requests.Session.request <http://docs.python-requests.org/en/master/api/#requests.Session.request>`__.
  [`#166 <https://github.com/MechanicalSoup/MechanicalSoup/pull/166>`__]

Internal changes:
-----------------

* ``StatefulBrowser.choose_submit`` will now ignore input elements that are
  missing a name-attribute instead of raising a ``KeyError``.
  [`#180 <https://github.com/MechanicalSoup/MechanicalSoup/issues/180>`__]

* Private methods ``Browser._build_request`` and ``Browser._prepare_request``
  have been replaced by a single method ``Browser._request``.
  [`#166 <https://github.com/MechanicalSoup/MechanicalSoup/pull/166>`__]

Version 0.9
===========

Main changes:
-------------

* We do not rely on BeautifulSoup's default choice of HTML parser.
  Instead, we now specify ``lxml`` as default. As a consequence, the
  default setting requires ``lxml`` as a dependency.

* Python 2.6 and 3.3 are no longer supported.

* The GitHub URL moved from
  https://github.com/hickford/MechanicalSoup/ to
  https://github.com/MechanicalSoup/MechanicalSoup. @moy and
  @hemberger are now officially administrators of the project in
  addition to @hickford, the original author.

* We now have a documentation site: https://mechanicalsoup.readthedocs.io/.
  The API is now fully documented, and we have included a tutorial,
  several more code examples, and a FAQ.

* ``StatefulBrowser.select_form`` can now be called without argument,
  and defaults to ``"form"`` in this case. It also has a new argument,
  ``nr`` (defaults to 0), which can be used to specify the index of
  the form to select if multiple forms match the selection criteria.

* We now use requirement files. You can install the dependencies of
  MechanicalSoup with e.g.::

    pip install -r requirements.txt -r tests/requirements.txt

* The ``Form`` class was restructured and has a new API. The behavior of
  existing code is unchanged, but a new collection of methods has been
  added for clarity and consistency with the ``set`` method:

  - ``set_input`` deprecates ``input``
  - ``set_textarea`` deprecates ``textarea``
  - ``set_select`` is new
  - ``set_checkbox`` and ``set_radio`` together deprecate ``check``
    (checkboxes are handled differently by default)

* A new ``Form.print_summary`` method allows you to write
  ``browser.get_current_form().print_summary()`` to get a summary of the
  fields you need to fill-in (and which ones are already filled-in).

* The ``Form`` class now supports selecting multiple options in
  a ``<select multiple>`` element.

Bug fixes
---------

* Checking checkboxes with ``browser["name"] = ("val1", "val2")`` now
  unchecks all checkbox except the ones explicitly specified.

* ``StatefulBrowser.submit_selected`` and ``StatefulBrowser.open`` now
  reset __current_page to None when the result is not an HTML page.
  This fixes a bug where __current_page was still the previous page.

* We don't error out anymore when trying to uncheck a box which
  doesn't have a ``checkbox`` attribute.

* ``Form.new_control`` now correctly overrides existing elements.

Internal changes
----------------

* The testsuite has been further improved and reached 100% coverage.

* Tests are now run against the local version of MechanicalSoup, not
  against the installed version.

* ``Browser.add_soup`` will now always attach a *soup*-attribute.
  If the response is not text/html, then soup is set to None.

* ``Form.set(force=True)`` creates an ``<input type=text ...>``
  element instead of an ``<input type=input ...>``.

Version 0.8
===========

Main changes:
-------------

* `Browser` and `StatefulBrowser` can now be configured to raise a
  `LinkNotFound` exception when encountering a 404 Not Found error.
  This is activated by passing `raise_on_404=True` to the constructor.
  It is disabled by default for backward compatibility, but is highly
  recommended.

* `Browser` now has a `__del__` method that closes the current session
  when the object is deleted.

* A `Link` object can now be passed to `follow_link`.

* The user agent can now be customized. The default includes
  `MechanicalSoup` and its version.

* There is now a direct interface to the cookiejar in `*Browser`
  classes (`(set|get)_cookiejar` methods).

* This is the last MechanicalSoup version supporting Python 2.6 and
  3.3.

Bug fixes:
----------

* We used to crash on forms without action="..." fields.

* The `choose_submit` method has been fixed, and the `btnName`
  argument of `StatefulBrowser.submit_selected` is now a shortcut for
  using `choose_submit`.

* Arguments to `open_relative` were not properly forwarded.

Internal changes:
-----------------

* The testsuite has been greatly improved. It now uses the pytest API
  (not only the `pytest` launcher) for more concise code.

* The coverage of the testsuite is now measured with codecov.io. The
  results can be viewed on:
  https://codecov.io/gh/hickford/MechanicalSoup

* We now have a requires.io badge to help us tracking issues with
  dependencies. The report can be viewed on:
  https://requires.io/github/hickford/MechanicalSoup/requirements/

* The version number now appears in a single place in the source code.

Version 0.7
===========

see Git history, no changelog sorry.
