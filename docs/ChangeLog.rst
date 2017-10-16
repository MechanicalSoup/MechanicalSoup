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

* We now have a documentation: http://mechanicalsoup.readthedocs.io/

* ``StatefulBrowser.select_form`` can now be called without argument,
  and defaults to ``"form"`` in this case.

* We now use requirement files. You can install the dependencies of
  Mechanicalsoup with e.g.::

    pip install -r requirements.txt -r tests/requirements.txt

Bug fixes
---------

* Checking checkboxes with ``browser["name"] = ("val1", "val2")`` now
  unchecks all checkbox except the ones explicitly specified.

* ``StatefulBrowser.submit_selected`` now resets __current_page even
  when the target of the form is not an HTML page.

* We don't error out anymore when trying to uncheck a box which
  doesn't have a ``checkbox`` attribute.

Internal Changes
----------------

* The testsuite has been further improved and reached 100% coverage.

* Tests are now ran against the local version of MechanicalSoup, not
  against the installed version.

Version 0.8
===========

Main changes:
-------------

* `Browser` and `StatefulBrowser` can now be configured to raise a
  `LinkNotFound` exception when encountering a 404 Not Found error.
  This is activated by passing `raise_on_404=True` to the constructor.
  It is disabled by default for backward compatibility, but is highly
  recommanded.

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
