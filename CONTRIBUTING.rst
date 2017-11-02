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

|Build Status| |Coverage Status|
|Requirements Status| |Documentation Status|
|CII Best Practices|

Python version support in the current master branch may differ from the
latest release in
`PyPI <https://pypi.python.org/pypi/MechanicalSoup/>`__. Please inspect
``.travis.yml`` or run ``python setup.py --classifiers`` to see which
versions of Python are supported in the current master branch.

Installing dependencies and running tests can be done with:

::

    python setup.py test

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

and

::

    virtualenv -p python2 --no-site-packages .virtual-py2 && source .virtual-py2/bin/activate
    pip install -r requirements.txt -r tests/requirements.txt

After making changes, run pytest in all virtualenvs:

::

    source .virtual-py3/bin/activate
    pytest

    source .virtual-py2/bin/activate
    pytest

Installation should be as simple as:

::

    python setup.py install

Release Checklist
-----------------

Releases can be done only by people with sufficient priviledges on
GitHub and PyPI. Things to do are:

At each release:

- Make sure all changes are documented in ``docs/ChangeLog.rst``
- Update the version number to $v in
  ``mechanicalsoup/__version__.py``
- Remove the ``(in development)`` mention in ``docs/ChangeLog.rst``.
- git commit -m "Release $v"
- git tag v$ver
- git push origin master v$v
- Visit the `release page on GitHub
  <https://github.com/MechanicalSoup/MechanicalSoup/releases>`__, copy
  the relevant section from ``docs/ChangeLog.rst`` to the release
  page.
- ``python setup.py sdist upload -r pypi`` or ``twine upload``. This
  requires a ``~/.pypirc`` with::

    [distutils]
    index-servers =
        pypi
    
    [pypi]
    username:<user>
    password:<password>

- Check on https://pypi.python.org/pypi/MechanicalSoup/

Right after the release:

- Update the version number to a ``x.y.z-dev`` number in
  ``mechanicalsoup/__version__.py``
- Create the ``(in development)`` section in ``docs/ChangeLog.rst``.
- ``git commit -m "Prepare for next release" && git push``

.. |Build Status| image:: https://travis-ci.org/MechanicalSoup/MechanicalSoup.svg?branch=master
   :target: https://travis-ci.org/MechanicalSoup/MechanicalSoup
.. |Coverage Status| image:: https://codecov.io/gh/MechanicalSoup/MechanicalSoup/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/MechanicalSoup/MechanicalSoup
.. |Requirements Status| image:: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements.svg?branch=master
   :target: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements/?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/mechanicalsoup/badge/?version=latest
   :target: https://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/1334/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/1334)
