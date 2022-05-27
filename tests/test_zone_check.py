from pytest import fixture

from dnszone.zone_check import ZoneCheck


@fixture
def zone():
    return ZoneCheck()


def test_zone_check_bad(zone, mocker):
    mocker.patch("dnszone.zone_check.subprocess.call", return_value=1)
    assert not zone.isValid("a", "b")
    assert zone.error == "Bad syntax"


def test_zone_check_good(zone, mocker):
    mocker.patch("dnszone.zone_check.subprocess.call", return_value=0)
    assert zone.isValid("a", "b")
    assert zone.error is None
