MechanicalSoup tutorial
=======================

The simplest way to use MechanicalSoup is to use
the :class:`~mechanicalsoup.StatefulBrowser` class (this example is
available as `example.py
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/example.py>`__
in MechanicalSoup's source code):

.. literalinclude:: ../example.py
   :language: python

Alternatively, one can use the :class:`~mechanicalsoup.Browser` class,
which doesn't maintain a state from one call to another (i.e. the
Browser itself doesn't remember which page you are visiting and what
is its content, it's up to the caller to do so). This example is
available as `example_manual.py
<https://github.com/MechanicalSoup/MechanicalSoup/blob/master/example_manual.py>`__
in the source:

.. literalinclude:: ../example_manual.py
   :language: python
