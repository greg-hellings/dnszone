from pytest import fixture, raises

from dnszone.zone_reload import ZoneReload, ZoneReloadError


@fixture
def zone():
    return ZoneReload()


def test_zone_reload_valid(zone, mocker):
    mocker.patch("dnszone.zone_reload.subprocess.call", return_value=0)
    assert zone.reload("a") is None


def test_zone_reload_invalid(zone, mocker):
    mocker.patch("dnszone.zone_reload.subprocess.call", return_value=1)
    with raises(ZoneReloadError):
        zone.reload("a")
