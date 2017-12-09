from bisect import bisect_right, bisect_left
from collections import OrderedDict
from enum import IntEnum, Enum

import math
from math import log10, floor

_MINIMUM_R_VALUE = 1e-200


class RenardSeriesKey(Enum):
    """An enumeration of possible Renard series identifiers.
    """
    R5 = (5, 0.01)
    R10 = (10, 0.01)
    R20 = (20, 0.01)
    R40 = (40, 0.01)
    R80 = (80, 0.01)

    RR10 = (10, 0.05)
    RR20 = (20, 0.05)
    RR40 = (40, 0.05)

    RRR5 = (5, 0.5)
    RRR10 = (10, 0.1)
    RRR20 = (20, 0.1)

    def __init__(self, cardinality, precision):
        self._cardinality = cardinality
        self._precision = precision

    @property
    def cardinality(self):
        return self._cardinality

    @property
    def precision(self):
        return self._precision




R5 = RenardSeriesKey.R5
R10 = RenardSeriesKey.R10
R20 = RenardSeriesKey.R20
R40 = RenardSeriesKey.R40
R80 = RenardSeriesKey.R80

RR10 = RenardSeriesKey.RR10
RR20 = RenardSeriesKey.RR20
RR40 = RenardSeriesKey.RR40


RRR5 = RenardSeriesKey.RRR5
RRR10 = RenardSeriesKey.RRR10
RRR20 = RenardSeriesKey.RRR20


_R = OrderedDict((
    (R5,  (1.00, 1.60, 2.50, 4.00, 6.30)),

    (R10, (1.00, 1.25, 1.60, 2.00, 2.50, 3.15, 4.00, 5.00, 6.30, 8.00)),

    (R20, (1.00, 1.12, 1.25, 1.40, 1.60, 1.80, 2.00, 2.24, 2.50, 2.80,
           3.15, 3.55, 4.00, 4.50, 5.00, 5.60, 6.30, 7.10, 8.00, 9.00)),

    (R40, (1.00, 1.06, 1.12, 1.18, 1.25, 1.32, 1.40, 1.50, 1.60, 1.70,
           1.80, 1.90, 2.00, 2.12, 2.24, 2.36, 2.50, 2.65, 2.80, 3.00,
           3.15, 3.35, 3.55, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.30,
           5.60, 6.00, 6.30, 6.70, 7.10, 7.50, 8.00, 8.50, 9.00, 9.50)),

    (R80, (1.00, 1.03, 1.06, 1.09, 1.12, 1.15, 1.18, 1.22, 1.25, 1.28,
           1.32, 1.36, 1.40, 1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75,
           1.80, 1.85, 1.90, 1.95, 2.00, 2.06, 2.12, 2.18, 2.24, 2.30,
           2.36, 2.43, 2.50, 2.58, 2.65, 2.72, 2.80, 2.90, 3.00, 3.07,
           3.15, 3.25, 3.35, 3.45, 3.55, 3.65, 3.75, 3.87, 4.00, 4.12,
           4.25, 4.37, 4.50, 4.62, 4.75, 4.87, 5.00, 5.15, 5.30, 5.45,
           5.60, 5.80, 6.00, 6.15, 6.30, 6.50, 6.70, 6.90, 7.10, 7.30,
           7.50, 7.75, 8.00, 8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75)),

    (RR10, (1.00, 1.25, 1.60, 2.00, 2.50, 3.20, 4.00, 5.00, 6.30, 8.00)),

    (RR20, (1.00, 1.10, 1.25, 1.40, 1.60, 1.80, 2.00, 2.20, 2.50, 2.80,
            3.20, 3.60, 4.00, 4.50, 5.00, 5.60, 6.30, 7.10, 8.00, 9.00)),

    (RR40, (1.00, 1.05, 1.10, 1.20, 1.25, 1.30, 1.40, 1.50, 1.60, 1.70,
            1.80, 1.90, 2.00, 2.10, 2.20, 2.40, 2.50, 2.60, 2.80, 3.00,
            3.20, 3.40, 3.60, 3.80, 4.00, 4.20, 4.50, 4.80, 5.00, 5.30,
            5.60, 6.00, 6.30, 6.70, 7.10, 7.50, 8.00, 8.50, 9.00, 9.50)),

    (RRR5,  (1.0, 1.5, 2.5, 4.0, 6.0)),

    (RRR10, (1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0)),

    (RRR20, (1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8,
             3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 9.0)),
))


def series(series_key):
    """The base values for the given Renard series.

    Args:
        series_key: An Renard series key such as R20.

    Returns:
        A tuple of base value for the series. For example, for
        R5 the tuple (1.00, 1.60, 2.50, 4.00, 6.30) will be returned.

    Raises:
        ValueError: If not such series exists.
    """
    try:
        return _R[series_key]
    except KeyError:
        raise ValueError("Renard series {} not found. Available Renard series keys are {}"
                         .format(series_key,
                                 ', '.join(str(key.name) for key in series_keys())))


def precision(series_key):
    """The precision for the given Renard series.

    Args:
        series_key: An Renard series key such as R20.

    Returns:
        The float multiple to which the base values in the series
        have been rounded.

    Raises:
        ValueError: If not such series exists.
    """
    if series_key not in _R:
        raise ValueError("Renard series {} not found. Available Renard series keys are {}"
                         .format(series_key,
                                 ', '.join(str(key.name) for key in series_keys())))
    return series_key.precision


def series_keys():
    """The available series keys.

    Note:
        The series keys returned will be members of the RenardSeriesKey enumeration.
        These are useful for programmatic use. For constant values consider
        using the module aliases R5, R10, R20, etc.

    Returns:
        A set-like object containing the series-keys.
    """
    return _R.keys()


def series_key_from_name(name):
    """Get an RenardSeriesKey from its name.

    Args:
        name: The series name as a string, for example 'R20'

    Returns:
        An RenardSeriesKey object which can be uses as a series_key.

    Raises:
        ValueError: If not such series exists.
    """
    try:
        return RenardSeriesKey[name]
    except KeyError:
        raise ValueError("Renard series with name {!r} not found. Available Renard series keys are {}"
                         .format(name,
                                 ', '.join(str(key.name) for key in series_keys())))


LOG10_MANTISSA_E = {num: list(map(lambda x: log10(x) % 1, series)) for num, series in _R.items()}

GEOMETRIC_SCALE_E = {num: max(b/a for a, b in zip(series, series[1:])) for num, series in _R.items()}


def find_greater_than_or_equal(series_key, value):
    """Find the smallest value greater-than or equal-to the given value.

    Args:
        series_key: An Renard series key such as R20.
        value: The query value.

    Returns:
        The smallest value from the specified series which is greater-than
        or equal-to the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in candidates:
        if candidate >= value:
            return candidate


def find_greater_than(series_key, value):
    """Find the smallest value greater-than or equal-to the given value.

    Args:
        series_key: An Renard series key such as R20.
        value: The query value.

    Returns:
        The smallest value from the specified series which is greater-than
        the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in candidates:
        if candidate > value:
            return candidate


def find_less_than_or_equal(series_key, value):
    """Find the largest value less-than or equal-to the given value.

    Args:
        series_key: An Renard series key such as R20.
        value: The query value.

    Returns:
        The largest value from the specified series which is less-than
        or equal-to the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in reversed(candidates):
        if candidate <= value:
            return candidate


def find_less_than(series_key, value):
    """Find the largest value less-than or equal-to the given value.

    Args:
        series_key: An Renard series key such as R20.
        value: The query value.

    Returns:
        The largest value from the specified series which is less-than
        the query value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    candidates = find_nearest_few(series_key, value, num=3)
    for candidate in reversed(candidates):
        if candidate < value:
            return candidate


def find_nearest(series_key, value):
    """Find the nearest value.

    Args:
        series_key: The RenardSeriesKey to use.
        value: The value for which the nearest value is to be found.

    Returns:
        The value in the specified Renard series closest to value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    return find_nearest_few(series_key, value, num=1)[0]


def find_nearest_few(series_key, value, num=3):
    """Find the nearest values.

    Args:
        series_key: The RenardSeriesKey to use.
        value: The value for which the nearest values are to be found.
        num: The number of nearby values to find: 1, 2 or 3.

    Returns:
        A tuple containing num values. With num == 3 it is guaranteed
        that  at least one item less than value, and one item greater
        than value.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If num is not 1, 2 or 3.
        ValueError: If value is not finite.
        ValueError: If value is out of range.
    """
    if num not in {1, 2, 3}:
        raise ValueError("num {} is not 1, 2 or 3".format(num))
    start = value / pow(GEOMETRIC_SCALE_E[series_key], 1.5)
    stop = value * pow(GEOMETRIC_SCALE_E[series_key], 1.5)
    candidates = tuple(rrange(series_key, start, stop))
    nearest = _nearest_n(candidates, value, num)
    return nearest


def rrange(series_key, start, stop):
    """Generate Renard values in a range inclusive of the start and stop values.

    Args:
        series_key: The RenardSeriesKey to use.
        start: The beginning of the range. The yielded values may include this value.
        stop: The end of the range. The yielded values may include this value.

    Yields:
        Values from the specified range which lie between the start and stop
        values inclusively, and in order from lowest to highest.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If start is not less-than or equal-to stop.
        ValueError: If start or stop are not both finite.
        ValueError: If start or stop are out of range.
    """
    if not math.isfinite(start):
        raise ValueError("Start value {} is not finite".format(start))
    if not math.isfinite(stop):
        raise ValueError("Stop value {} is not finite".format(stop))
    if start < _MINIMUM_R_VALUE:
        raise ValueError("{} is too small. The start value must greater than or equal to {}".format(stop, _MINIMUM_R_VALUE))
    if stop < _MINIMUM_R_VALUE:
        raise ValueError("{} is too small. The stop value must greater than or equal to {}".format(stop, _MINIMUM_R_VALUE))
    if not start <= stop:
        raise ValueError("Start value {} must be less than stop value {}".format(start, stop))

    return _rrange(series_key, start, stop)


def _rrange(series_key, start, stop):
    series_values = series(series_key)
    series_log = LOG10_MANTISSA_E[series_key]
    epsilon = (series_log[-1] - series_log[-2]) / 2
    start_log = log10(start) - epsilon
    start_decade, start_mantissa = _decade_mantissa(start_log)
    start_index = bisect_left(series_log, start_mantissa)
    if start_index == len(series_log):
        # Wrap to next decade
        start_decade += 1
        start_index = 0
    stop_log = log10(stop) + epsilon
    stop_decade, stop_mantissa = _decade_mantissa(stop_log)
    stop_index = bisect_right(series_log, stop_mantissa)
    assert stop_index != 0
    series_decade = int(log10(series_values[0]))
    for decade in range(start_decade, stop_decade + 1):
        index_begin = start_index if decade == start_decade else 0
        index_end = stop_index if decade == stop_decade else len(series_log)
        for index in range(index_begin, index_end):
            found = series_values[index]
            scale_exponent = decade - series_decade
            result = found * math.pow(10, scale_exponent)
            rounded_result = _round_sig(result, figures=series_decade + abs(floor(log10(series_key.precision))) + 1)
            if start <= rounded_result <= stop:
                yield rounded_result


def open_rrange(series_key, start, stop):
    """Generate Renard values in a half-open range inclusive of start, but exclusive of stop.

    Args:
        series_key: The RenardSeriesKey to use.
        start: The beginning of the range. The yielded values may include this value.
        stop: The end of the range. The yielded values will not include this value.

    Yields:
        Values from the specified range which lie in the half-open range defined by
        the start and stop values, from lowest to highest.

    Raises:
        ValueError: If series_key is not known.
        ValueError: If start is not less-than or equal-to stop.
        ValueError: If start or stop are not both finite.
        ValueError: If start or stop are out of range.
    """
    if not math.isfinite(start):
        raise ValueError("Start value {} is not finite".format(start))
    if not math.isfinite(stop):
        raise ValueError("Stop value {} is not finite".format(stop))
    if start < _MINIMUM_R_VALUE:
        raise ValueError("{} is too small. The start value must greater than or equal to {}".format(stop, _MINIMUM_R_VALUE))
    if stop < _MINIMUM_R_VALUE:
        raise ValueError("{} is too small. The stop value must greater than or equal to {}".format(stop, _MINIMUM_R_VALUE))
    if not start <= stop:
        raise ValueError("Start value {} must be less than stop value {}".format(start, stop))
    return (item for item in rrange(series_key, start, stop) if item != stop)


def _nearest_n(candidates, value, n):
    abs_deltas = tuple(abs(c - value) for c in candidates)
    indexes = [index for index, _ in sorted(enumerate(abs_deltas), key=lambda x: x[1])]
    nearest_three = tuple(sorted(candidates[i] for i in indexes[:n]))
    return nearest_three


def _round_sig(x, figures=6):
    return 0 if x == 0 else round(x, figures - floor(log10(abs(x))) - 1)


def _decade_mantissa(value):
    f_decade, mantissa = divmod(value, 1)
    return int(f_decade), mantissa



