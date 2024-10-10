import pytest

from repository.repository import get_all_crashes, get_all_daily_crashes, get_all_weekly_crashes, \
    get_all_monthly_crashes, get_all_areas, get_all_injuries_by_area, get_all_crash_causes, get_daily_crashes_by_date, \
    get_weekly_crashes_by_date, get_injuries_by_area, get_monthly_crashes_by_date


def test_get_all_crashes():
    res = get_all_crashes()
    assert len(res) > 0


def test_get_all_daily_crashes():
    res = get_all_daily_crashes()
    assert len(res) >= 0


def test_get_all_weekly_crashes():
    res = get_all_weekly_crashes()
    assert len(res) >= 0


def test_get_all_monthly_crashes():
    res = get_all_monthly_crashes()
    assert len(res) >= 0


def test_get_all_areas():
    res = get_all_areas()
    assert len(res) >= 0


def test_get_all_injuries_by_area():
    res = get_all_injuries_by_area()
    assert len(res) >= 0


def test_get_all_crash_causes():
    res = get_all_crash_causes()
    assert len(res) >= 0


def test_get_daily_crashes_by_date():
    res = get_daily_crashes_by_date("9/5/2023 19:05")
    assert False


def test_get_weekly_crashes_by_date():
    res = get_weekly_crashes_by_date("9/5/2023 19:05")
    assert False

def test_get_monthly_crashes_by_date():
    res = get_monthly_crashes_by_date("9/5/2023 19:05")
    assert False

def test_injury_area():
    res = get_injuries_by_area("225")
    assert True