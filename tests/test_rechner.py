from src.rechner import summe, durchschnitt, prozent


def test_summe():
    assert summe(10, 5) == 15


def test_durchschnitt():
    assert durchschnitt(10, 20) == 15


def test_prozent():
    assert prozent(200, 10) == 20