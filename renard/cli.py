"""The command-line for renard"""

import os
import sys

import docopt
import docopt_subcommands as dsc

from renard.eng import eng_string
from renard.version import __version__
from renard.renard import (series_key_from_name, find_nearest, find_nearest_few, find_greater_than_or_equal,
                           find_greater_than, find_less_than, find_less_than_or_equal,  series, rrange)

DOC_TEMPLATE = """{program}

Usage: {program} [options] <command> [<args> ...]

Options:
  -h --help     Show this screen.
  -v --verbose  Use verbose logging

Available commands:
  {available_commands}

See '{program} help <command>' for help on specific commands.
"""


@dsc.command()
def handle_nearest(args):
    """usage: {program} nearest <e-series> <value> [--symbol]

    The nearest value in an Renard series.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_nearest(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_nearby(args):
    """usage: {program} nearby <e-series> <value> [--symbol]

    At least three nearby values in an Renard series, and least one of
    which will be less-than the given value, and at least one
    greater-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearby_few = find_nearest_few(series_key, value)
    for item in nearby_few:
        item_text = present_value(args, item)
        print(item_text)
    return os.EX_OK


@dsc.command()
def handle_gt(args):
    """usage: {program} gt <e-series> <value> [--symbol]

    The largest value greater-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_greater_than(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_ge(args):
    """usage: {program} ge <e-series> <value> [--symbol]

    The largest value greater-than or equal-to the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_greater_than_or_equal(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_lt(args):
    """usage: {program} lt <e-series> <value> [--symbol]

    The largest value less-than the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_less_than(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_le(args):
    """usage: {program} le <e-series> <value> [--symbol]

    The largest value less-than or equal-to the given value.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    value = extract_value(args)
    nearest = find_less_than_or_equal(series_key, value)
    nearest_text = present_value(args, nearest)
    print(nearest_text)
    return os.EX_OK


@dsc.command()
def handle_tolerance(args):
    """usage: {program} tolerance <e-series> [--symbol]

    The tolerance of the given Renard series.

    Options:
     -s --symbol  Display as a percentage.
    """
    series_key = extract_series_key(args)
    tol = tolerance(series_key)
    if args['--symbol']:
        percent = float(tol * 100)
        if percent.is_integer():
            percent = int(percent)
        print("{}%".format(percent))
    else:
        print(tol)
    return os.EX_OK

@dsc.command()
def handle_series(args):
    """usage: {program} series <e-series>

    The base values for the given Renard series.
    """
    series_key = extract_series_key(args)
    for item in series(series_key):
        print(item)
    return os.EX_OK


@dsc.command()
def handle_range(args):
    """usage: {program} range <e-series> <start-value> <stop-value> [--symbol]

    All values in the given Renard series from start-value to stop-value inclusive.

    Options:
      -s --symbol  Use the SI magnitude prefix symbol.
    """
    series_key = extract_series_key(args)
    start_value = extract_value(args, '<start-value>')
    stop_value = extract_value(args, '<stop-value>')
    items = rrange(series_key, start_value, stop_value)
    for item in items:
        item_text = present_value(args, item)
        print(item_text)
    return os.EX_OK


def present_value(args, nearest):
    return eng_string(nearest, prefix=args['--symbol'])


def extract_series_key(args):
    e_series_name = args['<e-series>']
    series_key = series_key_from_name(e_series_name)
    return series_key


def extract_value(args, name='<value>'):
    text_value = args[name]
    try:
        value = float(text_value)
    except ValueError:
        raise ValueError("{!r} could not be interpreted as an Renard series {}".format(
            text_value, name[1:-1]))
    return value


def main(argv=None):
    try:
        return dsc.main(
            program='renard',
            version='Renard series {}'.format(__version__),
            argv=argv,
            doc_template=DOC_TEMPLATE,
            exit_at_end=False)
    except docopt.DocoptExit as exc:
        print(exc, file=sys.stderr)
        return os.EX_USAGE
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return os.EX_DATAERR


if __name__ == '__main__':
    sys.exit(main())
