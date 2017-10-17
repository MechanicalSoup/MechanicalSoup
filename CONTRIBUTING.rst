Overall Guidelines
------------------

Bug reports, feature suggestions and pull requests welcome. 

When editing please don't reformat code—this makes diffs and pull requests hard to read.

Hints on Development
--------------------

|Build Status| |Coverage Status|
|Requirements Status| |Documentation Status|

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

.. |Build Status| image:: https://travis-ci.org/MechanicalSoup/MechanicalSoup.svg?branch=master
   :target: https://travis-ci.org/MechanicalSoup/MechanicalSoup
.. |Coverage Status| image:: https://codecov.io/gh/MechanicalSoup/MechanicalSoup/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/MechanicalSoup/MechanicalSoup
.. |Requirements Status| image:: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements.svg?branch=master
   :target: https://requires.io/github/MechanicalSoup/MechanicalSoup/requirements/?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/mechanicalsoup/badge/?version=latest
   :target: http://mechanicalsoup.readthedocs.io/en/latest/?badge=latest
