import os

from renard.cli import main


def test_nearest(capfd):
    code = main("nearest R10 21".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "20\n"


def test_nearest_with_symbol(capfd):
    code = main("nearest R10 21000 -s".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "20 k\n"


def test_nearby(capfd):
    code = main("nearby R20 31".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "28\n31.5\n35.5\n"


def test_gt(capfd):
    code = main("gt R20 31".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "31.5\n"


def test_lt(capfd):
    code = main("lt R20 31".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "28\n"


def test_ge(capfd):
    code = main("ge R20 40".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "40\n"


def test_le(capfd):
    code = main("le R20 40".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "40\n"


def test_series_r3(capfd):
    code = main("series R5".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "1.0\n1.6\n2.5\n4.0\n6.3\n"


def test_range_R10(capfd):
    code = main("range R10 1700 3400".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "2e3\n2.5e3\n3.15e3\n"


def test_range_R10_symbol(capfd):
    code = main("range R10 1700 3400 -s".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == "2 k\n2.5 k\n3.15 k\n"


def test_bogus_r_series_gives_exit_code_ex_dataerr():
    code = main("series R13".split())
    assert code == os.EX_DATAERR


def test_bogus_value_gives_exit_code_ex_dataerr():
    code = main("nearest R10 FOO".split())
    assert code == os.EX_DATAERR


def test_malformed_command_gives_code_ex_usage():
    code = main("foo R13 316".split())
    assert code == os.EX_USAGE


def test_precision(capfd):
    code = main("precision R5".split())
    out, err = capfd.readouterr()
    assert code == os.EX_OK
    assert out == '0.01\n'

def test_bogus_r_series_precision_gives_exit_code_ex_dataerr():
    code = main("series R13".split())
    assert code == os.EX_DATAERR
