=============
Release Notes
=============

Version 0.9 (in development)
============================

Main changes:
-------------

* Python 2.6 and 3.3 are no longer supported.

* The GitHub URL moved from
  https://github.com/hickford/MechanicalSoup/ to
  https://github.com/MechanicalSoup/MechanicalSoup. @moy and
  @hemberger are now officially administrators of the project in
  addition to @hickford, the original author.

* We now have a documentation: https://mechanicalsoup.readthedocs.io/

* ``StatefulBrowser.select_form`` can now be called without argument,
  and defaults to ``"form"`` in this case.

* We now use requirement files. You can install the dependencies of
  Mechanicalsoup with e.g.::

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

Internal Changes
----------------

* The testsuite has been further improved and reached 100% coverage.

* Tests are now run against the local version of MechanicalSoup, not
  against the installed version.

* ``Browser.add_soup`` will now always attach a *soup*-attribute.
  If the response is not text/html, then soup is set to None.

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
