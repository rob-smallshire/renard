renard
======

The Renard series are a system of preferred numbers used in
engineering applications which specify a geometric sequence
of numbers over the range one to ten. The numbers
are selected to be convenient to use and to minimise the
maximum relative error when an arbitrary number is replaced
by the nearest Renard number. The series were proposed by the
French army engineer Colonel Charles Renard and subsequently
standardised in ISO 3-1973.

For example, the R5 series contains six values
(1.0, 1.6, 2.5, 4.0, 6.3) which cover a single order-of-magnitude
range of values (one decade) from one to ten.
These base values repeat again to cover the next decade from 10
to 100, as 10, 16, 25, 40, and 63.

This ``renard`` library is useful for selecting values from the
least rounded R5, R10, R20, R40 and R80 decades, the medium
rounded RR10, RR20 and RR40 decades, and the most rounded RRR5,
RRR10 and RRR20 decades.



Status
------

.. image:: https://travis-ci.org/rob-smallshire/renard.svg?branch=master
    :target: https://travis-ci.org/rob-smallshire/renard

.. image:: https://coveralls.io/repos/github/rob-smallshire/renard/badge.svg?branch=master
    :target: https://coveralls.io/github/rob-smallshire/renard?branch=master



Installation
------------

The ``renard`` package is available on the Python Package Index (PyPI):

.. image:: https://badge.fury.io/py/renard.svg
    :target: https://badge.fury.io/py/renard

The package supports Python 3 only. To install::

  $ pip install renard

Python Interface
----------------

For full help::

  >>> import renard
  >>> help(renard)

In the meantime, here are some highlights.

To find the nearest R20 value to 319 use::

  >>> from renard import find_nearest, R20
  >>> find_nearest(R20, 319)
  315.0


To find the next value greater-than or equal-to 182 in the R80 series
use::

  >>> from renard import find_greater_than_or_equal, R80
  >>> find_greater_than_or_equal(R80, 182)
  185.0

To find a few values around the specified value, use::

  >>> from renard import find_nearest_few, R20
  >>> find_nearest_few(R20, 5000)
  (4500.0, 5000.0, 5600.0)


Command-Line Interface
----------------------

There's also a handy command-line interface. Run ``renard --help``
to see a list of commands::

  $ renard --help
  renard

  Usage: renard [options] <command> [<args> ...]

  Options:
    -h --help     Show this screen.
    -v --verbose  Use verbose logging

  Available commands:
    ge
    gt
    help
    le
    lt
    nearby
    nearest
    range
    series
    precision


  See 'renard help <command>' for help on specific commands.


To find a nearby value, use::

  $ renard nearest R20 37726
  35.5e3

If you prefer an SI exponent symbol, supply ``--symbol`` or ``-s``::

  $ renard nearest R20 37726 -s
  35.5 k

To show values around the given value, use the ``nearby`` command::

  $ renard nearby R40 52e6 -s
  50 M
  53 M
  56 M

To show the smallest value greater than or equal to the given value, use the ``ge`` command::

  $ renard ge R40 52e3 -s
  53 k

To show all values in an inclusive range, use the ``range`` command::

  $ renard range R5 74e-9 34e-6 -s
  100 n
  160 n
  250 n
  400 n
  630 n
  1 µ
  1.6 µ
  2.5 µ
  4 µ
  6.3 µ
  10 µ
  16 µ
  25 µ

To use the most-rounded Renard R"20 series (for syntactic reasons, R'20 is called
RR20 and R" is called RRR20 on the command line)::

  $ renard range RRR20 10000 20000
  10e3
  11e3
  12e3
  14e3
  16e3
  18e3
  20e3


To determine the multiple to which the base values of a series have
been rounded, use the ``precision`` command::

  $ renard precision R5
  0.01


