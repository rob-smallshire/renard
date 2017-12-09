import math
from hypothesis import given, assume
from hypothesis.strategies import sampled_from, floats, data, integers
from pytest import raises

from renard.renard import (RenardSeriesKey, series, rrange, find_less_than_or_equal, find_greater_than_or_equal,
                           find_nearest,
                           find_less_than, find_greater_than, find_nearest_few, open_rrange, R10, precision)


@given(series_key=sampled_from(RenardSeriesKey))
def test_series_cardinality(series_key):
    assert len(series(series_key)) == series_key.cardinality


@given(series_key=sampled_from(RenardSeriesKey),
       low=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_rrange_cardinality_over_one_order_of_magnitude(series_key, low):
    high = low * 10.0
    assume(math.isfinite(high))
    values = list(rrange(series_key, low, high))
    include_end = bool(high in values)
    cardinality = series_key.cardinality + include_end
    assert len(values) == cardinality


@given(series_key=sampled_from(RenardSeriesKey),
       low=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False),
       high=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_rrange_strictly_ordered(series_key, low, high):
    assume(low < high)
    values = list(rrange(series_key, low, high))
    assert all(values[i] < values[i+1] for i in range(len(values)-1))


@given(series_key=sampled_from(RenardSeriesKey),
       low=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_open_rrange_cardinality_over_one_order_of_magnitude(series_key, low):
    high = low * 10.0
    assume(math.isfinite(high))
    values = list(open_rrange(series_key, low, high))
    cardinality = series_key.cardinality
    assert len(values) == cardinality


@given(series_key=sampled_from(RenardSeriesKey),
       low=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False),
       high=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_open_rrange_strictly_ordered(series_key, low, high):
    assume(low < high)
    values = list(open_rrange(series_key, low, high))
    assert all(values[i] < values[i+1] for i in range(len(values)-1))


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_less_than_or_equal(series_key, value):
    assert find_less_than_or_equal(series_key, value) <= value


@given(data())
def test_less_than_or_equal_returns_value_from_series(data):
    series_key = data.draw(sampled_from(RenardSeriesKey))
    value = data.draw(sampled_from(series(series_key)))
    assert find_less_than_or_equal(series_key, value) == value


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_less_than(series_key, value):
    assert find_less_than(series_key, value) < value


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_greater_than_or_equal(series_key, value):
    assert find_greater_than_or_equal(series_key, value) >= value


@given(data())
def test_greater_than_or_equal_returns_value_from_series(data):
    series_key = data.draw(sampled_from(RenardSeriesKey))
    value = data.draw(sampled_from(series(series_key)))
    assert find_greater_than_or_equal(series_key, value) == value

@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_greater_than(series_key, value):
    assert find_greater_than(series_key, value) > value


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_find_nearest_in_range(series_key, value):
    nearest = find_nearest(series_key, value)
    assert find_less_than_or_equal(series_key, value) <= nearest <= find_greater_than_or_equal(series_key, value)


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_find_nearest_is_nearest(series_key, value):
    nearest = find_nearest(series_key, value)
    lower = find_less_than_or_equal(series_key, value)
    upper = find_greater_than_or_equal(series_key, value)
    assert (((nearest == lower) and (nearest - lower <= upper - nearest))
            or ((nearest == upper) and (upper - nearest <= nearest - lower)))


@given(data())
def test_nearest_returns_value_from_series(data):
    series_key = data.draw(sampled_from(RenardSeriesKey))
    value = data.draw(sampled_from(series(series_key)))
    assert find_nearest(series_key, value) == value


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False),
       num=sampled_from((1, 2, 3)))
def test_find_nearest_few_has_correct_cardinality(series_key, value, num):
    assert len(find_nearest_few(series_key, value, num)) == num


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False),
       num=integers())
def test_find_nearest_few_raises_error_with_num_out_of_range(series_key, value, num):
    assume(num not in {1, 2, 3})
    with raises(ValueError):
        find_nearest_few(series_key, value, num)


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_find_nearest_three_includes_at_least_one_less(series_key, value):
    assert any(v < value for v in find_nearest_few(series_key, value))


@given(series_key=sampled_from(RenardSeriesKey),
       value=floats(min_value=1e-35, max_value=1e35, allow_nan=False, allow_infinity=False))
def test_find_nearest_three_includes_at_least_one_greater(series_key, value):
    assert any(v > value for v in find_nearest_few(series_key, value))


def test_erange_start_infinite_raises_value_error():
    with raises(ValueError):
        inf = float("inf")
        rrange(R10, inf, 10)


def test_erange_stop_infinite_raises_value_error():
    with raises(ValueError):
        rrange(R10, 10, float("inf"))


def test_erange_start_too_small_raises_value_error():
    with raises(ValueError):
        rrange(R10, 0, 10)


def test_erange_stop_too_small_raises_value_error():
    with raises(ValueError):
        rrange(R10, 10, 0)


def test_erange_start_stop_in_wrong_order_raises_value_error():
    with raises(ValueError):
        rrange(R10, 10, 8)


def test_open_erange_start_infinite_raises_value_error():
    with raises(ValueError):
        inf = float("inf")
        open_rrange(R10, inf, 10)


def test_open_erange_stop_infinite_raises_value_error():
    with raises(ValueError):
        open_rrange(R10, 10, float("inf"))


def test_open_erange_start_too_small_raises_value_error():
    with raises(ValueError):
        open_rrange(R10, 0, 10)


def test_open_erange_stop_too_small_raises_value_error():
    with raises(ValueError):
        open_rrange(R10, 10, 0)


def test_open_erange_start_stop_in_wrong_order_raises_value_error():
    with raises(ValueError):
        open_rrange(R10, 10, 8)


def test_illegal_series_key_raises_value_error():
    with raises(ValueError):
        series(13)


@given(series_key=sampled_from(RenardSeriesKey))
def test_series_precision_is_positive(series_key):
    assert precision(series_key) > 0


def test_illegal_precision_series_key_raises_value_error():
    with raises(ValueError):
        precision(object())


