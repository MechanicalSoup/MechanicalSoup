Overall Guidelines
------------------

Bug reports, feature suggestions and pull requests welcome (on
GitHub). Security issues should be reported by email to the core
developers (emails available in the "Author" field of commits in the
Git history).

When editing please don't reformat code—this makes diffs and pull
requests hard to read.

Code should be flake8-clean and the test coverage is and should remain
100%. Add new tests whenever you add new features.

Hints on Development
--------------------

|Build Status|
|Coverage Status|
|Documentation Status|
|CII Best Practices|

Python version support in the current main branch may differ from the
latest release in
`PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__. Please inspect our
`GitHub Actions workflows <https://github.com/MechanicalSoup/MechanicalSoup/actions>`__

Installing dependencies and running tests can be done with:

::

    pip install -r requirements.txt
    pip install -r tests/requirements.txt
    pytest

The documentation can be generated and viewed with:

::

    pip install sphinx
    python setup.py build_sphinx
    firefox docs/_build/html/index.html

The documentation is generated from docstrings within ``*.py`` files,
and ``*.rst`` documentation files in the ``docs/`` directory.

You can develop against multiple versions of Python using
`virtualenv <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>`__:

::

    python3 -m venv .virtual-py3 && source .virtual-py3/bin/activate
    pip install -r requirements.txt -r tests/requirements.txt

After making changes, run pytest in all virtualenvs:

::

    source .virtual-py3/bin/activate
    pytest

Installation should be as simple as:

::

    python setup.py install

Editing the logo
----------------

The logo is available as an SVG file in ``assets/``. You may need to
install the `Open Sans
<https://fonts.google.com/specimen/Open+Sans>`__ and `Zilla Slab
<https://fonts.google.com/specimen/Zilla+Slab>`__ fonts (download and
store the ``*.ttf`` files in your ``~/.local/share/fonts`` directory)
to view it properly. The file can then be opened in e.g. Inkscape.

Release Checklist
-----------------

Releases can be done only by people with sufficient privileges on
GitHub and PyPI. Things to do are:

At each release:

-  Make all final changes to the repository before release:

   - Document all notable changes in ``docs/ChangeLog.rst``.
   - Update the version number to X.Y.Z in ``mechanicalsoup/__version__.py``.
   - Remove the ``(in development)`` mention in ``docs/ChangeLog.rst``.

- Commit and push the release to GitHub (both branch and tag)::

    git commit -m "Release X.Y.Z"
    git branch vX.Y
    git tag vX.Y.Z
    git push origin main vX.Y vX.Y.Z

- Visit the `release page on GitHub
  <https://github.com/MechanicalSoup/MechanicalSoup/releases>`__, copy
  the relevant section from ``docs/ChangeLog.rst`` to the release
  page.

- Wait for the "Upload Python Package" GitHub Action to complete, and then
  check on https://pypi.org/project/MechanicalSoup/. Verify installation
  from PyPI with ``pip install --no-cache-dir mechanicalsoup``.

Right after the release:

- Update the version number to a ``X.Y.Z-dev`` number in
  ``mechanicalsoup/__version__.py``
- Create a new ``(in development)`` section in ``docs/ChangeLog.rst``.
- ``git commit -m "Prepare for next release" && git push``

.. |Build Status| image:: https://github.com/MechanicalSoup/MechanicalSoup/actions/workflows/python-package.yml/badge.svg?branch=main
   :target: https://github.com/MechanicalSoup/MechanicalSoup/actions/workflows/python-package.yml?query=branch%3Amain
.. |Coverage Status| image:: https://codecov.io/gh/MechanicalSoup/MechanicalSoup/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/MechanicalSoup/MechanicalSoup
.. |Documentation Status| image:: https://readthedocs.org/projects/mechanicalsoup/badge/?version=latest
   :target: https://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/1334/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/1334
